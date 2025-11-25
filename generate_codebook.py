data = [  ("Economic and Employment", "Fair Market Rent", "ho7_FIPS_2010", "float64", "Fips code for 2010"),
    ("Economic and Employment", "Fair Market Rent", "ho7_STNAME", "object", "State name"),
    ("Economic and Employment", "Fair Market Rent", "ho7_countyname", "object", "County name"),
    ("Economic and Employment", "Fair Market Rent", "ho7_fmr_0", "int64", "Fair Market Rent for an Efficiency"),
    ("Economic and Employment", "Fair Market Rent", "ho7_fmr_1", "int64", "Fair Market Rent for a 1-bedroom unit"),
    ("Economic and Employment", "Fair Market Rent", "ho7_fmr_2", "int64", "Fair Market Rent for a 2-bedroom unit"),
    ("Economic and Employment", "Fair Market Rent", "ho7_fmr_3", "int64", "Fair Market Rent for a 3-bedroom unit"),
    ("Economic and Employment", "Fair Market Rent", "ho7_fmr_4", "int64", "Fair Market Rent for a 4-bedroom unit"),
    ("Economic and Employment", "Fair Market Rent", "ho7_pop2010", "float64", "2010 Census population"),
    ("Economic and Employment", "Fair Market Rent", "ho7_fmr_type", "int64", "40th/50th percentile indicator"),]
    
data2 = [("Economic and Employment", "USA Spending", "ec9_FIPS_2010", "int64", "Fips code for 2010"),
    ("Economic and Employment", "USA Spending", "ec9_State", "object", "State name"),
    ("Economic and Employment", "USA Spending", "ec9_CTYNAME", "object", "County name"),
    ("Economic and Employment", "USA Spending", "ec9_Total_Prime_Award", "float64", "Total prime award count"),
    ("Economic and Employment", "USA Spending", "ec9_Total_Sub_Award", "float64", "Total subaward count"),]

for category, subcategory, var, type, description in data:
    print(f"""<tr data-domain="Housing">
        <td><a href="#" onclick="goToDomainSection('Housing')">{category}</a></td>
        <td>{subcategory}</td>
        <td>HUD Fair Market Rent (2000-2025)</td> 
        <td>{var}</td>
        <td>{type}</td>
        <td>{description}</td>
        </tr>""")
    
for category2, subcategory2, var2, type2, description2 in data2:
    print(f"""<tr data-domain="Economics">
        <td><a href="#" onclick="goToDomainSection('Economics')">{category2}</a></td>
        <td>{subcategory2}</td>
        <td>Custom Award Data</td> 
        <td>{var2}</td>
        <td>{type2}</td>
        <td>{description2}</td>
        </tr>""")
