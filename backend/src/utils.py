def simpleQueryToList(query):
  return [row.to_dict for row in query]

def complexQueryToList(query):
  results = []
  for row in query:
    r = dict(row._mapping)
    obj = {}
    for col in r.values():
      obj.update(col.to_dict)
    results.append(obj)
  
  return results

def oldQueryToDict(query):
  return {"results": [dict(row._mapping) for row in query]}