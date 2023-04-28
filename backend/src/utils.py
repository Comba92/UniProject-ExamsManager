def resultToDict(queryResult):
  return {"results": [dict(row._mapping) for row in queryResult]}

def filterBy(queryResult, column, value):
  d = resultToDict(queryResult)
  f = list(filter(lambda tupla: tupla[column] == value, d["results"]))
  return { "results": f }