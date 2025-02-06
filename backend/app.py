from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 模拟书籍数据
books = [
    {"id": "book1", "name": "理性", "description": "当代思想家史蒂芬·平克在《理性》这本书中回答了所有关于理性的问题。平克否定了“人类是非理性的，人类仅仅是充满了偏见、谬误和错觉的穴居人”这一陈词滥调。目录：第一章 动物有多理性；第二章 理性与非理性；第三章 逻辑与批判性思维；第四章 概率与随机性；第五章 信念与证据：贝叶斯推理；第六章 风险与回报：理性选择与预期效用；第七章 正确反应与误报：信号检测与统计决策理论……"},
    {"id": "book2", "name": "理商", "description": "只要简单罗列一下，就不难发现，现代生活离不开理性的决策和选择。然而不幸的是，现代世界所处的情境往往是我们大脑进化出的默认认知系统难以适应的，所以我们必须超越直觉和经验，根据这些对大脑很不友好的信息来做出理性的判断和决定。理性思维正如智力一样，也是可测量的认知能力，但标准的智力测验并不能很好地测量理性思维的任何一个组成部分——适应性反应、良好的判断力和良好的决策能力。目录：第一章 哲学、认知科学和民间对理性的定义；第二章 理性、智力和心智的功能结构；第三章 避免吝啬加工：检测、压制和心智资源；第四章 理性思维综合评估测验框架；第五章 概率与统计推理；第六章 科学推理；第七章 避免吝啬加工：直接测量……"},
    {"id": "book3", "name": "思考，快与慢", "description": "人类究竟有多理性？在书中，卡尼曼会带领我们体验一次思维的终极之旅。目录：第1章 一张愤怒的脸和一道乘法题；第2章 电影的主角与配角；第3章 惰性思维与延迟满足的矛盾；第4章 联想的神奇力量；第5章 你的直觉有可能只是错觉；第6章 意料之外与情理之中；第7章 字母“B”与数字“13”……"},
    {"id": "book4", "name": "超越智商", "description": "高智商，就意味着能做出正确的、好的决策？错！研究表示，公认的聪明人在决策的正确率方面与普通人无异。目录：导读 理性：重新定义人类认知能力；第1章乔治•布什的心智：有关智力测验缺失什么的线索；第2章理性障碍：理性与智力的分离；第3章反省心智、算法心智与自主心智；第4章 给智力概念瘦身；第5章为何聪明人常做蠢事；第6章认知吝啬鬼；第7章决策效应与认知吝啬鬼……"},
    {"id": "book5", "name": "心智探奇", "description": "《心智探奇》权威解答“什么是智能”这一深刻问题，破解机器人难题。详细剖析心智的四大能力，权威解读“心智如何工作”。一扇窥视人类心智活动神奇与奥秘的窗户。一场探索心智本质的奇幻之旅。目录：第一章 心智是什么；第二章 心智计算理论；第三章 自然选择理论；第四章 心智能力1：视觉感知；第五章 心智能力2：推理；第六章 心智能力3：情感；第七章 心智能力4：社会关系；结语 活出生命的意义"},
    {"id": "book6", "name": "机器人叛乱", "description": "你有两个毫无人性的主人，一个是基因，一个是模因。它们寄生在你身上，你懵懂无知地为你的主人卖命，哪怕为此丢了脑袋也在所不惜。目录：第1章 踏入达尔文的无底洞；第2章 跟自己作战的大脑；第3章 机器人的秘密武器；第4章 自发式大脑偏差；第5章 进化心理学出了什么问题；第6章 理性障碍；第7章 才出狼窝，又入虎穴……"},
    {"id": "book7", "name": "有限理性", "description": "本书是承续诺贝尔经济学奖获得者赫伯特·A.西蒙开创的有限理性观。目录：第1章 对理性的再思考；第2章 什么是有限理性；第3章 适应性工具箱；第4章 适用于受环境限制头脑的快速节俭启发式；第5章 有限理性的进化性适应和经济学概念；第6章 小组报告：适应性工具箱有根据吗……"}
]

# 计算书籍相似度
def calculate_similarity(books):
    descriptions = [book["description"] for book in books]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix

# 获取相关书籍
@app.route('/related_books', methods=['GET'])
def related_books():
    book_id = request.args.get('book_id')
    similarity_matrix = calculate_similarity(books)
    nodes = [{"id": book["id"], "name": book["name"]} for book in books]
    links = []
    for i, book in enumerate(books):
        if book["id"] == book_id:
            for j, sim in enumerate(similarity_matrix[i]):
                if sim > 0.9 and j != i:  # 相似度大于0.9的书籍
                    links.append({"source": book["id"], "target": books[j]["id"]})
    return jsonify({"nodes": nodes, "links": links})

# 搜索书籍
@app.route('/search', methods=['GET'])
def search():
    book_name = request.args.get('book_name')
    result = [book for book in books if book_name in book["name"]]
    return jsonify(result)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)