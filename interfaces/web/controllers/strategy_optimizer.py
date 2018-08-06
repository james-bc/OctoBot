from flask import render_template, request, jsonify

from interfaces.web import server_instance
from interfaces.web.models.strategy_optimizer import get_strategies_list, get_current_strategy, get_time_frames_list, \
    get_evaluators_list, get_risks_list, start_optimizer, get_optimizer_results
from interfaces.web.util.flask_util import get_rest_reply


@server_instance.route("/strategy-optimizer")
@server_instance.route('/strategy-optimizer', methods=['GET', 'POST'])
def strategy_optimizer():
    if request.method == 'POST':
        update_type = request.args["update_type"]
        request_data = request.get_json()
        success = False
        reply = "Operation OK"

        if request_data:
            if update_type == "start_optimizer":
                try:
                    strategy = request_data["strategy"]
                    time_frames = request_data["time_frames"]
                    evaluators = request_data["evaluators"]
                    risks = request_data["risks"]
                    start_optimizer(strategy, time_frames, evaluators, risks)
                    success = True
                    reply = "Strategy optimizer launched"
                except Exception as e:
                    return get_rest_reply('{"start_optimizer": "ko: '+e+'"}', 500)

        if success:
            # TODO
            return get_rest_reply(jsonify(reply))
        else:
            return get_rest_reply('{"update": "ko"}', 500)

    elif request.method == 'GET':
        if request.args:
            target = request.args["target"]
            if target == "strategy_optimizer_results":
                optimizer_results = get_optimizer_results()
                return get_rest_reply(jsonify(optimizer_results))

        else:
            return render_template('strategy-optimizer.html',
                                   strategies=get_strategies_list(),
                                   current_strategy=get_current_strategy(),
                                   time_frames=get_time_frames_list(),
                                   evaluators=get_evaluators_list(),
                                   risks=get_risks_list())
