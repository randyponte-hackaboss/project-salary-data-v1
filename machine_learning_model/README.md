# jobs-salary-extraction
API de extracción de salarios


## Estructura:
- src: contiene el código fuente con utils y el **api.py** que tiene la lógica de API.
- notebooks: notebooks con **ejemplos** para consumir y manipular la respuesta de la API.
- cache: Contiene el resultado de ejecuciones previas. Esto es por si el proceso falla por algún motivo no sea necesario volver a enviar a chat-gpt lo mismo **reduciendo el costo en caso de falla**.


## Build
docker build -t api .


## Run
docker run --rm --name api-container -p 3000:3000 -e CHAT_GPT_API_KEY='<KEY_API_OPEN-AI>' --mount type=bind,source="$(pwd)/cache",target=/cache api




## Notas:
- La key no queda guardada.
- La caché es un diccionario en caso de querer invalidar una entrada pueden remover la key. Si lo borran no hay problema se vuelve a recrear. Incluso si se encuentra ejecutando.


## Ejemplo de uso con curl
```
curl -d '{"description": <texto de aviso>, "jobid":<id del job>, "location":<país o código>}' -H "Content-Type: application/json" -X POST localhost:3000/predict
```


## Explicacion de campos:
- min y max: Es el rango salarial.
- currency: La moneda del aviso.
- time_lampse: Periodo de pago.
- reduce_description: Es el texto que se envía. Es para debugear.
- source: Si responde Chat-GPT, alguna regla o viene de caché.
- token_count_sent_chat_gpt: Cuantos tokens enviamos.
- cost: costo por este request.


## Ejemplos:


### Ejemplo con rango salarial en el aviso salario:
```
curl -d '{"description": "rango salarial entre 30 a 40 por hora", "jobid":1, "location":"arg"}' -H "Content-Type: application/json" -X POST localhost:3000/predict
```


### Respuesta:
```
{"cost":0.00094,"currency":"ARS","max":40.0,"min":30.0,"reduce_description":"salarial entre 30 a 40 30 a 40 por hora arg","source":"Chat-Gpt","time_lapse":"hour","token_count_sent_chat_gpt":620}
```


### Ejemplo sin salario:
```
curl -d '{"description": "rango salarial a convenir segun experiencia", "jobid":2, "location":"arg"}' -H "Content-Type: application/json" -X POST localhost:3000/predict
```
### Respuesta
```
{"cost":0.0,"currency":" ","max":0.0,"min":0.0,"reduce_description":" ","source":"Not-sent-to-chat-gpt","time_lapse":" ","token_count_sent_chat_gpt":0.0}
```


En este caso el costo es **0**, ya que se envía nada(**"token_count_sent_chat_gpt":0.0**) a chat-gpt.


En reduce_description no vemos texto alguno eso es porque no hay números ergo no hay contexto asociado para enviarle nada a chat-gpt.


## Ejemplo mas rebuscado:
```
curl -d '{"description": "rango salarial a convenir segun experiencia a partir de 2.5m sin primas. Bonos de 500k", "jobid":3, "location":"colombia"}' -H "Content-Type: application/json" -X POST localhost:3000/predict
```
### respuesta:
```
{"cost":0.0009465000000000001,"currency":"COP","max":2500000.0,"min":2500000.0,"reduce_description":"partir de 2.5m sin primas. bonos de 500k colombia","source":"Chat-Gpt","time_lapse":"month","token_count_sent_chat_gpt":624}
```


min y max son iguales porque no hay rango.
Tampoco cae en la trampa del bono que no forma parte del salario base que queremos extraer.

