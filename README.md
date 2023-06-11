# labdb-ecommerce
### API example:
curl "http://localhost:5000/query?db=postgres&query=SELECT%20*%20FROM%20users%20WHERE%20id%20=%201"

curl "http://localhost:5000/query?db=mongo&query={%22find%22:%20%22users%22,%20%22filter%22:%20{%22id%22:%201}}"

curl "http://localhost:5000/query?db=neo4j&query=MATCH%20(n)%20RETURN%20n%20LIMIT%2025"
