def valid_range(salary_min, time_lapse, currency):
    if currency.lower()=="usd" or currency.lower()=="eur":
        if time_lapse=="month":
            return salary_min >= 900
        if time_lapse=="day":
            return salary_min >= 240 and salary_min < 320
        if time_lapse=="year":
            return salary_min < 250000 and salary_min >= 15000
        if time_lapse=="hour":
            return salary_min >= 15 and salary_min < 140
        if time_lapse=="week":
            return salary_min >= 600

    return True