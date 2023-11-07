import os
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number
from langchain.chat_models import ChatOpenAI
from src.textprocessing.preprocess import normalize_text, remove_punctuation

openai_api_key = os.environ["CHAT_GPT_API_KEY"]

salary_schema = Object(
    id="salary",
    
    description="Job's salary with period of payment and currency",
    attributes=[
        Number(
            id="salary_range_min",
            description="bottom of the salary range",
        ),
        Number(
            id="salary_range_max",
            description="maximum of the salary range",
        ),
        Text(
            id="payment_period",
            descriptio="period of payment"
        ),
        Text(id="currency",
             description="salary currency"
        )
    ],

    examples=[
        # Chile
        (normalize_text("20,000,00 - 40,000,00"), {"salary_range_min":2000000, "salary_range_max":4000000, "time_lapse":"month", "currency": "CLP"}),
        (normalize_text("renta: $600.000"), {"min":600000, "max":600000, "payment_period":"month", "currency": "CLP"}),
        
        #Colombia
        (normalize_text("$2.200.000 - $2.500.000 al mes"), {"salary_range_min":2200000, "salary_range_max":2500000, "time_lapse":"month", "currency": "COP"}),
        (normalize_text("$3'300.000 cop"), {"min":3300000, "max":3300000, "payment_period":"month", "currency": "COP"}),

        #Mexico
        (normalize_text("$20,000.00 - $40,000.00 al mes"), {"salary_range_min":20000, "salary_range_max":40000, "payment_period":"month", "currency": "MXN"}),

        #Argentina
        (normalize_text("$550.000,00 - $850.000,00 al mes"), {"salary_range_min":550000, "salary_range_max":850000, "payment_period":"month", "currency": "ARS"}),

        #Guatemala
        (normalize_text("q11,000 a q20,000"), {"salary_range_min":11000, "salary_range_max":20000, "payment_period":"month", "currency": "GTQ"}),

        # Republica dominicana
        (normalize_text("rd$40,000-rd$80,000."), {"salary_range_min":40000, "salary_range_max":80000, "payment_period":"month", "currency": "DOP"}),

        # usd year
        # range is between $50-70.
        (normalize_text("range is between $50-70k."), {"salary_range_min":50000, "salary_range_max":70000, "payment_period":"year", "currency": "USD"}),

        (normalize_text("range is between $5-9k."), {"salary_range_min":5000, "salary_range_max":9000, "payment_period":"month", "currency": "USD"})
    ],
    many=False
)

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    max_tokens=1000,
    request_timeout=60,
    openai_api_key=openai_api_key,
    model_kwargs={"frequency_penalty":0,"presence_penalty":0, "top_p": 1.0}
)

chain = create_extraction_chain(llm,
                                salary_schema)
