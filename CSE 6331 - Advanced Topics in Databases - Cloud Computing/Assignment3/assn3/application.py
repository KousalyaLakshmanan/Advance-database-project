"""Cloud Foundry test"""
from flask import Flask, current_app, render_template, request, redirect, url_for
import os, json, datetime, random
from azuredb import connect
from azureredis import r

app = Flask(__name__)

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

# default
@app.route('/', methods=["GET"])
def hello_world():
	# return render_template('index.html', result=obj)
	return render_template('index.html')


@app.route('/prob1', methods=["POST"])
def problem_1():

	query_count = int(request.form["query_count"])
	use_cache = (request.form["use_cache"] == "True")

	total_time = 0

	for i in range(query_count):

		if (use_cache):
			# cache
			if r.exists("all"):
				# start time
				start_time = datetime.datetime.now().timestamp()

				result = json.loads(r.get("all"))

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)
			else:

				# start time
				start_time = datetime.datetime.now().timestamp()

				sql = "SELECT place from quakes"
				cursor = connect.cursor()
				cursor.execute(sql)
				output = cursor.fetchall()

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

				result = []
				for row in output:
					result.append(row[0])

				r.set("all", json.dumps(result))
			
		else:
			# no cache

			# start time
			start_time = datetime.datetime.now().timestamp()

			cursor = connect.cursor()
			sql = "SELECT place from quakes"
			cursor.execute(sql)
			output = cursor.fetchall()

			# end time
			total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

			result = []
			for row in output:
				result.append(row[0])

	total_time = total_time * 1000
	return render_template('prob2.html', query_count=query_count, use_cache=use_cache, execution_time=total_time)


@app.route('/prob2', methods=["POST"])
def problem_2():
	start_magnitude = int(request.form["start_magnitude"])
	end_magnitude = int(request.form["end_magnitude"])

	query_count = int(request.form["query_count"])
	use_cache = (request.form["use_cache"] == "True")

	total_time = 0

	for i in range(query_count):
		magnitude = round(random.uniform(start_magnitude, end_magnitude), 1)

		if (use_cache):
			# cache
			if r.exists("mag=" + str(magnitude)):
				# start time
				start_time = datetime.datetime.now().timestamp()

				result = json.loads(r.get("mag=" + str(magnitude)))

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)
			else:

				# start time
				start_time = datetime.datetime.now().timestamp()

				sql = "SELECT place from quakes where mag = ?"
				cursor = connect.cursor()
				cursor.execute(sql, (magnitude))
				output = cursor.fetchall()

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

				result = []
				for row in output:
					result.append(row[0])

				r.set("mag=" + str(magnitude), json.dumps(result))
			
		else:
			# no cache

			# start time
			start_time = datetime.datetime.now().timestamp()

			cursor = connect.cursor()
			sql = "SELECT place from quakes where mag = ?"
			cursor.execute(sql, (magnitude))
			output = cursor.fetchall()

			# end time
			total_time + (datetime.datetime.now().timestamp() - start_time)

			result = []
			for row in output:
				result.append(row[0])

	total_time = total_time * 1000
	return render_template('prob2.html', query_count=query_count, use_cache=use_cache, execution_time=total_time)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)



