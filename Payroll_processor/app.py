import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse


app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    df = pd.read_excel(file.filename, index_col=0)
    df['TOTAL_INCOME'] = (df["BASIC"] + df["HOUSING"] + df["TRANSPORT"] +df["MEAL"]) * 12
    df['PENSION'] = ((df["BASIC"] + df["HOUSING"] + df["TRANSPORT"]) * 0.08) * 12
    df['NHF'] =  (df["BASIC"] * 0.025) * 12
    df['GROSS_INCOME'] = df['TOTAL_INCOME'] - (df['PENSION'] + df['NHF'])

    if((0.01 * df['GROSS_INCOME'])>200000).any():
        df['CRA'] = (0.01 * df['GROSS_INCOME']) + (0.2 * df['GROSS_INCOME'])
    else:
        df['CRA'] = 200000 + (0.2 * df['GROSS_INCOME'])
    df['CHARGEABLE_INCOME'] = df['TOTAL_INCOME'] - (df['PENSION'] + df['NHF'] +  df['CRA'])

    if(df['CHARGEABLE_INCOME']< 300000).any():
        df['1ST'] = df['CHARGEABLE_INCOME'] * 0.01
    else:
        df['1ST'] = 0.07 * 300000

    if((df['CHARGEABLE_INCOME']-300000)>= 300000 ).any():
        df['2ND'] = 300000 * 0.11
    elif((df['CHARGEABLE_INCOME']-300000)< 0).any():
            df['2ND'] = 0
    else:
        df['2ND'] = (df['CHARGEABLE_INCOME'] - 300000) * 0.11
    
    #df.to_json(orient="split")
    return df.to_excel("output6.xlsx")