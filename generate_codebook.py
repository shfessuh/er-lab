data = [
    ("Housing", "Mortgage Lending", "int64", "ho2_NUM_ORIGINATIONS"),
    ("Housing", "Mortgage Lending", "int64", "ho2_AMT_ORIGINATIONS"),
    ("Housing", "Mortgage Lending", "int64", "ho2_NUM_CONVENTIONAL"),
    ("Housing", "Mortgage Lending", "int64", "ho2_AMT_CONVENTIONAL"),
    ("Housing", "Mortgage Lending", "int64", "ho2_NUM_GOVERNMENT"),
    ("Housing", "Mortgage Lending", "int64", "ho2_AMT_GOVERNMENT"),
    ("Housing", "Mortgage Lending", "int64", "ho2_NUM_FHA"),
    ("Housing", "Mortgage Lending", "int64", "ho2_AMT_FHA"),
    ("Housing", "Mortgage Lending", "int64", "ho2_NUM_VA"),
    ("Housing", "Mortgage Lending", "int64", "ho2_AMT_VA"),
    ("Housing", "Mortgage Lending", "int64", "ho2_NUM_RHS_FSA"),
    ("Housing", "Mortgage Lending", "int64", "ho2_AMT_RHS_FSA"),
    ("Housing", "Mortgage Lending", "int64", "ho2_NUM_HOME_PURCHASE"),
    ("Housing", "Mortgage Lending", "int64", "ho2_AMT_HOME_PURCHASE"),
    ("Housing", "Mortgage Lending", "int64", "ho2_NUM_HOME_IMPROVEMENT"),
    ("Housing", "Mortgage Lending", "int64", "ho2_AMT_HOME_IMPROVEMENT"),
    ("Housing", "Mortgage Lending", "int64", "ho2_NUM_REFINANCE"),
    ("Housing", "Mortgage Lending", "int64", "ho2_AMT_REFINANCE"),
]

for category, subcategory, data, var, in data:
    print(f"""<tr data-domain="Housing">
        <td><a href="#" onclick="goToDomainSection('Housing')">{category}</a></td>
        <td>{subcategory}</td>
        <td>NaNDA (1981-2024) Home Mortgage Disclosure Act</td>
        <td>{var}</td>
        <td>{data}</td>
        <td></td>
        </tr>""")