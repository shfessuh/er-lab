import json
import os
import pandas as pd
import numpy as np
from shapely.geometry import shape, mapping
from shapely.affinity import translate, scale
from shapely.geometry import box as shapely_box
from shapely.ops import unary_union
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df_year = pd.read_csv("FinalVariable_CountyPolicies_DATASET2018_analysis_1108.csv")
df_year = df_year[df_year['year'] == 2010]
with open("georef-united-states-of-america-county.json") as f:
    geo = json.load(f)

counties = []
for item in geo:
    geom = shape(item["geo_shape"]["geometry"])
    geom = geom.simplify(0.01, preserve_topology=True)
    counties.append({
        "FIPS": str(item["coty_code"][0]).zfill(5),
        "ste_name": item["ste_name"][0],
        "coty_name": item["coty_name"][0],
        "geometry": geom
    })
del geo

features = [
    'HigherEdMerge', 'Prc_Agric_Merge', 'Prc_Const_Merge', 'Prc_Manufac_Merge',
    'MHHIncome_Merge', 'Prc_ForeignBorn_Merge', 'Prc_LatinoPop_Merge',
    'Prc_UnemployTotal_Merge', 'Prc_UnemployCivilian_Merge',
    'ViolentCrimeRate_Merge', 'Prc_Poverty_Merge',
    'Count_LatElectOfficial', 'Count_Undocumented'
]
cluster_df = df_year[["FIPS", "State", "County"] + features + ["TotalPopMerge"]].dropna(subset=features)
for col in features:
    mask = cluster_df[col] >= 999999
    if mask.any():
        cluster_df.loc[mask, col] = cluster_df.loc[~mask, col].mean()

scaler = StandardScaler()
kmeans = KMeans(n_clusters=2, random_state=42)
cluster_df["cluster"] = kmeans.fit_predict(scaler.fit_transform(cluster_df[features]))
centers = pd.DataFrame(kmeans.cluster_centers_, columns=features)
cluster_df["FIPS"] = cluster_df["FIPS"].astype(str).str.zfill(5)

INDEX_DEFINITIONS = {
    "economic_hardship": {
        "label": "Economic Hardship",
        "description": "Combines poverty, unemployment, and (inverted) median income. "
                       "Higher score = more economic hardship.",
        "variables": ["Prc_Poverty_Merge", "Prc_UnemployTotal_Merge",
                      "Prc_UnemployCivilian_Merge", "MHHIncome_Merge"],
        "flip": ["MHHIncome_Merge"],
    },
    "demographic_composition": {
        "label": "Latino/Foreign-Born Composition",
        "description": "Combines Latino and foreign-born population shares. "
                       "Higher score = greater share of these populations.",
        "variables": ["Prc_LatinoPop_Merge", "Prc_ForeignBorn_Merge",
                      "Count_Undocumented"],
        "flip": [],
    },
    "industry_profile": {
        "label": "Goods-Producing Industry",
        "description": "Combines employment shares in agriculture, construction, "
                       "and manufacturing. Higher score = more goods-producing economy.",
        "variables": ["Prc_Agric_Merge", "Prc_Const_Merge", "Prc_Manufac_Merge"],
        "flip": [],
    },
    "education": {
        "label": "Educational Attainment",
        "description": "Share of adults with higher education. "
                       "Higher score = higher educational attainment.",
        "variables": ["HigherEdMerge"],
        "flip": [],
    },
    "civic_power": {
        "label": "Civic Power",
        "description": "Count of Latino elected officials. "
                       "Higher score = more Latino political representation.",
        "variables": ["Count_LatElectOfficial"],
        "flip": [],
    },
    "public_safety": {
        "label": "Violent Crime Burden",
        "description": "Violent crime rate. Higher score = higher crime burden.",
        "variables": ["ViolentCrimeRate_Merge"],
        "flip": [],
    },
}


def build_index(df, variables, flip=None, min_fraction=0.5):
    """
    Build a composite index from a list of variables.

    Method: percentile-rank each variable (0-1), flip direction where needed,
            average across variables, rescale to 0-100.
    """
    flip = flip or []
    ranks = df[variables].rank(pct=True)
    for v in flip:
        ranks[v] = 1 - ranks[v]
    min_vars = max(1, int(len(variables) * min_fraction))
    present = df[variables].notna().sum(axis=1)
    avg = ranks.mean(axis=1) * 100
    avg[present < min_vars] = np.nan
    return avg

for key, cfg in INDEX_DEFINITIONS.items():
    cluster_df[f"idx_{key}"] = build_index(
        cluster_df,
        variables=cfg["variables"],
        flip=cfg["flip"],
    )
    valid = cluster_df[f"idx_{key}"].notna().sum()
    print(f"  {cfg['label']}: {valid} counties scored")

cluster_lookup = {}
pop_lookup = {}
index_lookup = {}

for _, row in cluster_df.iterrows():
    fips = row["FIPS"]
    cluster_lookup[fips] = int(row["cluster"])
    if pd.notnull(row.get("TotalPopMerge")):
        pop_lookup[fips] = int(row["TotalPopMerge"])
    index_lookup[fips] = {
        key: (round(float(row[f"idx_{key}"]), 1) if pd.notnull(row[f"idx_{key}"]) else None)
        for key in INDEX_DEFINITIONS
    }

feature_labels = {
    'HigherEdMerge': 'Higher Education', 'Prc_Agric_Merge': '% Agriculture',
    'Prc_Const_Merge': '% Construction', 'Prc_Manufac_Merge': '% Manufacturing',
    'MHHIncome_Merge': 'Median HH Income', 'Prc_ForeignBorn_Merge': '% Foreign Born',
    'Prc_LatinoPop_Merge': '% Latino Pop.', 'Prc_UnemployTotal_Merge': '% Unemployed (Total)',
    'Prc_UnemployCivilian_Merge': '% Unemployed (Civ.)', 'ViolentCrimeRate_Merge': 'Violent Crime Rate',
    'Prc_Poverty_Merge': '% Poverty', 'Count_LatElectOfficial': 'Latino Elected Officials',
    'Count_Undocumented': 'Undocumented Count',
}

cluster_info = {}
for i in range(kmeans.n_clusters):
    top = centers.iloc[i].abs().sort_values(ascending=False).head(5)
    cluster_info[i] = {
        "topDrivers": {
            feature_labels.get(k, k): round(float(centers.iloc[i][k]), 3)
            for k in top.index
        },
        "countyCount": int((cluster_df["cluster"] == i).sum()),
    }
county_features = {}
for _, row in cluster_df.iterrows():
    county_features[row["FIPS"]] = {
        feature_labels.get(f, f): round(float(row[f]), 3) if pd.notnull(row[f]) else None
        for f in features
    }

territories = ["Puerto Rico", "American Samoa", "United States Virgin Islands",
               "Guam", "Commonwealth of the Northern Mariana Islands"]

mainland_counties = [c for c in counties if c["ste_name"] not in territories and not c["FIPS"].startswith(("02", "15"))]
alaska_counties = [c for c in counties if c["FIPS"].startswith("02")]
hawaii_counties = [c for c in counties if c["FIPS"].startswith("15")]
clip_box = shapely_box(-170, 50, -129, 72)
for c in alaska_counties:
    c["geometry"] = c["geometry"].intersection(clip_box)
alaska_counties = [c for c in alaska_counties if not c["geometry"].is_empty]

ak_union = unary_union([c["geometry"] for c in alaska_counties])
ak_cx, ak_cy = ak_union.centroid.x, ak_union.centroid.y
for c in alaska_counties:
    c["geometry"] = translate(
        scale(c["geometry"], xfact=0.55, yfact=0.55, origin=(ak_cx, ak_cy)),
        xoff=35, yoff=-53
    )

ak_xs = [c["geometry"].bounds[0] for c in alaska_counties] + [c["geometry"].bounds[2] for c in alaska_counties]
ak_ys = [c["geometry"].bounds[1] for c in alaska_counties] + [c["geometry"].bounds[3] for c in alaska_counties]
ak_bounds = [min(ak_xs), min(ak_ys), max(ak_xs), max(ak_ys)]
hi_clip = shapely_box(-161, 18.5, -154.5, 22.5)
for c in hawaii_counties:
    c["geometry"] = c["geometry"].intersection(hi_clip)
hawaii_counties = [c for c in hawaii_counties if not c["geometry"].is_empty]

hi_union = unary_union([c["geometry"] for c in hawaii_counties])
hi_cx, hi_cy = hi_union.centroid.x, hi_union.centroid.y
for c in hawaii_counties:
    c["geometry"] = scale(c["geometry"], xfact=2.8, yfact=2.8, origin=(hi_cx, hi_cy))

hi_xs = [c["geometry"].bounds[0] for c in hawaii_counties] + [c["geometry"].bounds[2] for c in hawaii_counties]
hi_ys = [c["geometry"].bounds[1] for c in hawaii_counties] + [c["geometry"].bounds[3] for c in hawaii_counties]
hi_bounds_raw = [min(hi_xs), min(hi_ys), max(hi_xs), max(hi_ys)]

x_shift = (ak_bounds[2] + 0.3) - hi_bounds_raw[0]
y_shift = (ak_bounds[1] + ak_bounds[3]) / 2 - (hi_bounds_raw[1] + hi_bounds_raw[3]) / 2
for c in hawaii_counties:
    c["geometry"] = translate(c["geometry"], xoff=x_shift, yoff=y_shift)

all_counties = mainland_counties + alaska_counties + hawaii_counties

geojson_features = []
for c in all_counties:
    fips = c["FIPS"]
    props = {
        "FIPS": fips,
        "name": c["coty_name"],
        "state": c["ste_name"],
        "cluster": cluster_lookup.get(fips),
        "pop": pop_lookup.get(fips),
    }
    idx_values = index_lookup.get(fips, {})
    for key in INDEX_DEFINITIONS:
        props[f"idx_{key}"] = idx_values.get(key)

    geojson_features.append({
        "type": "Feature",
        "properties": props,
        "geometry": mapping(c["geometry"])
    })

geojson = {"type": "FeatureCollection", "features": geojson_features}

def round_coords(coords, precision=4):
    if isinstance(coords[0], (list, tuple)):
        return [round_coords(c, precision) for c in coords]
    return [round(c, precision) for c in coords]

for feat in geojson["features"]:
    geom = feat["geometry"]
    if geom["type"] in ("Polygon", "MultiPolygon"):
        geom["coordinates"] = round_coords(geom["coordinates"])
with open("counties.geojson", "w") as f:
    json.dump(geojson, f, separators=(',', ':'))

indicator_meta = {
    feature_labels.get(v, v): {"key": v, "label": feature_labels.get(v, v)}
    for v in features
}

meta = {
    "clusterInfo": cluster_info,
    "clusterLabels": {str(i): f"Typology {chr(65 + i)}" for i in range(kmeans.n_clusters)},
    "clusterColors": {"0": "#E85D75", "1": "#4ECDC4", "2": "#FFB84D",
                      "3": "#8B5CF6", "4": "#10B981"},
    "indexDefinitions": {
        key: {
            "label": cfg["label"],
            "description": cfg["description"],
            "variables": [feature_labels.get(v, v) for v in cfg["variables"]],
        }
        for key, cfg in INDEX_DEFINITIONS.items()
    },
    "countyFeatures": county_features,
    "indicatorMeta": indicator_meta,
    "insetBounds": {
        "akBounds": ak_bounds,
        "hiBounds": [min([c["geometry"].bounds[0] for c in hawaii_counties]),
                     min([c["geometry"].bounds[1] for c in hawaii_counties]),
                     max([c["geometry"].bounds[2] for c in hawaii_counties]),
                     max([c["geometry"].bounds[3] for c in hawaii_counties])],
        "pad": 0.9
    }
}

with open("cluster_data.json", "w") as f:
    json.dump(meta, f, separators=(',', ':'))

geo_size = os.path.getsize("counties.geojson") / 1024 / 1024
meta_size = os.path.getsize("cluster_data.json") / 1024 / 1024
