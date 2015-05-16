from data_parser import BTCNetwork
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
# configuration
DEBUG = True
SECRET_KEY = 'ucsc clustering'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def home():
    return render_template('index.html', context={})

@app.route("/get_btn", methods=['POST'])
def get_btn():
    btn_address = request.form['btn_address']

    if not btn_address:
        flash('Please enter a valid bitcoin address')
        return redirect(url_for('home'))

    btc = BTCNetwork()
    data = btc.data_parse(origin=btn_address)

    return jsonify(nodes=data[0], links=data[1])

@app.route("/get_cluster", methods=['POST'])
def get_cluster():
    origin = request.form['origin_addr']

    if not origin:
        flash('Please enter a valid bitcoin address')
        return redirect(url_for('home'))

    btc = BTCNetwork()
    nodes, links = btc.data_parse(origin=origin)

    clustered_nodes, clustered_links, number_of_clusters = btc.data_clust(origin, nodes, links)
    return jsonify(nodes=clustered_nodes, links=clustered_links, number_of_clusters=number_of_clusters)


#if __name__=="__main__":
#    app.run()
    #btc = BTCNetwork()
    #origin = '17z35xHz19KcdnxDGH9awSsqxSYSLeu35T'
    #nodes, links = btc.data_parse(origin=origin)
    #clustered_nodes, clustered_links, number_of_clusters = btc.data_clust(origin, nodes, links)