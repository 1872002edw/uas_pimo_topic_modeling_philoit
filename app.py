from flask import Flask, render_template, request, json, jsonify, send_file
import split_tanggal
import clustering

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/find")
def find():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    split_tanggal.getCSV(start_date,end_date)
    topics_dict = clustering.do_cluster(start_date,end_date)
    return json.dumps(topics_dict)
   

@app.route("/detail")
def detail():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    topic = request.args.get('topic')
    path = f'static/wordclouds/{start_date}_{end_date}_topic{topic}.png'
    return render_template('detail.html', imagepath = path)

@app.route("/history")
def history():
    return render_template('history.html')

@app.route("/download")
def download():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    path = split_tanggal.getCSV(start_date,end_date)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run()