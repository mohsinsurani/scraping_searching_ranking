from flask import Flask, render_template, request, jsonify
# import crawl
import search_pub
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/result", methods=['POST', "GET"])
def result():
    output = request.form.to_dict()
    text = output["name"]
    print("search text is", text)
    results = search_pub.search(text)
    # json_file = {}
    # json_file['query'] = results
    return render_template("index.html",name = text)

    # return jsonify(json_file)


@app.route("/search", methods=['POST', "GET"])
def searchRoute():
    print("came in search")
    global resp

    if request.method == "POST":
        req_data = request.data
        print("post is", request.data)
        # req_data = request.form.get('query')
        req_data = request.data.decode(encoding='UTF-8', errors='ignore')
        # req_data = json.load(deco)
        print("data is", req_data)
        query = req_data
        results = search_pub.search_pub(query)
        print("success")
        json_file = {}
        json_file['result'] = results
        response = jsonify(results)
        response.headers.add("Access-Control-Allow-Origin", "*")
        print(jsonify(json_file))
        print("ssssfskjndfgalskjghasljkg")
        return response

# print(name)
# exit()
# return render_template("index.html",name = name)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
