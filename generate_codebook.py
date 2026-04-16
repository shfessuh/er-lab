data = [
    ("Job Oppurtunities", "w1_jo_md", "US Census County Business Patterns", "This dataset provides county-level data on business establishments, employment, and industry composition. It supports analyses of local economic structure and labor markets." ),
    ("Job Oppurtunities","w3_jo_md", "BLS Quarterly Census of Employment and Wages", "This dataset from the U.S. Bureau of Labor Statistics’ Quarterly Census of Employment and Wages (QCEW) provides county-level data on employment, establishments, and wages, supporting analysis of local labor market structure and economic conditions." ),
    ("Unions", "w4_unions_md", "Office of Labor Management Standards Online Public Disclosure", "This dataset contains union financial disclosures and governance records from the U.S. Department of Labor’s Office of Labor-Management Standards. It supports analyses of labor organization activity and transparency."  )

]
  
for subdomain, id, name, description in data: 
    print(f""" <section id="{id}" class ="metadata" style="display:none;">
                <div class ="metadata_banner">
                <div class ="metadata_banner_buttons">
                <h2 class="metadata_header">{name}</h2>
                <button class="metadata_back" onclick="hideMetaData(); return false;"><i class="fa-solid fa-angle-left"></i></button>
                </div>
                </div>
                <div class ="metadata_content">
                  <div metadata_inline_headings>
                 <p class="datasource_desc">{description}</p>
                  <h3 class="domain-dataset-headers">Description of Data Processing</h3>
                  <p>DATA PROCESSING DESCRIPTION GOES HERE Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo onsequat.</p>
                 </div>
                 <div class ="boxes_metadata">
                  <div class = "domain-dropdown">
                  <h1 class="metadata_domain"><strong>Domain: </strong>Work</h1>
                  <button class="md_back" onclick="toggleBoxDesc(); return false;"><i class="fa-solid fa-angle-left"></i></button>
                  </div>
                  <div class="metadata_drop_content" style="display: block">
                  <p class="box_desc" style="display: block">These datasets measures the structure of local labor markets  industry composition, job growth, wage levels, and union density . These indicators capture whether the jobs available in a county come with economic security, health benefits, and worker protections, and whether workers have collective bargaining power, all of which determine the material conditions that mediate structural drivers and health outcomes.</p>
                  </div>
                   <div class = "subdomain-dropdown">
                  <h1 class="metadata_subdomain"><strong>Subdomain: </strong>{subdomain}]</h1>
                  <button class="back" onclick="toggleBoxDesc(); return false;"><i class="fa-solid fa-angle-left"></i></button>
                  </div>
                  <div class="metadata_drop_content" style="display: block">
                  <p class = "sd_drop_content_desc" style="display: block">desc</p>
                  </div>
                </div>
                </div>
          </section>""")