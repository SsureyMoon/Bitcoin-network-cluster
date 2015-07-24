# Bitcoin network drawer
This wep application has two functions.

1. Aggregating history of bitcoin addresses of a given bitcoin address and drawing of the bitcoin network.
2. Finding clusters of the bitcoin network from 1 and showing them in different colors.

Only nodes, which are two transactions away from the origin address, are available.
*Limitation: It shows only small enough networks to get all nodes of in 20 seconds.

```bash
virtualenb <your virtual env>
pip install -r requirements.txt
```
Go to `https://bitbucket.org/taynaud/python-louvain` and install the library by running:
```bash
python the/folder/you/download/the/above/setup.py install
```
In local mode: `gunicorn server:app --timeout 20`
##Demo
On Heroku: http://arcane-fjord-8360.herokuapp.com/
##Reference

- Web framework: Flask(http://flask.pocoo.org/), Gunicorn(http://gunicorn.org/)
- Data source: Blockchain.info(https://blockchain.info/)
- Clustering libraries: NetworkX(https://networkx.github.io/), Community Detection(http://perso.crans.org/aynaud/communities/)
- Visualization libraries: D3.js(http://d3js.org/), Interactive Force Directed Graph(https://gist.github.com/pkerpedjiev/0389e39fad95e1cf29ce), Bootstrap3(http://getbootstrap.com/)
