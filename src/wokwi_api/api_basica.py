from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LeituraRequest(BaseModel):
    bueiro: float or None
    leito: float or None
    rele: bool or None


@app.post("/")
def receber_leitura(item: LeituraRequest):
    # Aqui, "item" já é um objeto LeituraRequest, convertido do JSON enviado
    print('leitura recebida:')
    print(item)

    return {
        "status": "success",
        "message": "Leitura recebida com sucesso",
        "data": item.model_dump_json()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8180)