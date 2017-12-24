#
"""
var url_ping =                       "/ping"
var url_machines =                   "/machines"
var url_machine =                    "/machines/:machine_name"
var url_check_invalid_machine_name = "/machines/:machine_name/*"
var url_processes =                  "/machines/:machine_name/processes/"
var url_process =                    "/machines/:machine_name/processes/:process_name"
var url_check_invalid_process_name = "/machines/:machine_name/processes/:process_name/*"
//var url_if =                       "/machines/:machine_name/processes/:process_name/if"
var url_ifs =                        "/machines/:machine_name/processes/:process_name/:if_kind(if_numbers|if_messages|if_logs|if_arrows|if_toggles|if_buttons|if_videos)"
var url_ifs_all =                        "/machines/:machine_name/processes/:process_name/ifs"
var url_if =                         "/machines/:machine_name/processes/:process_name/:if_kind(if_numbers|if_messages|if_logs|if_arrows|if_toggles|if_buttons|if_videos)/:if_name"
var url_machine_disable_rules =      "/machines/:machine_name/disable_rules/*"
var url_machine_hiding_rules =       "/machines/:machine_name/hiding_rules/*"
var url_process_disable_rules =      "/machines/:machine_name/processes/:process_name/disable_rules/*"
var url_process_hiding_rules =       "/machines/:machine_name/processes/:process_name/hiding_rules/*"
var url__if_disable_rules =          "/machines/:machine_name/processes/:process_name/:if_kind(if_numbers|if_messages|if_logs|if_arrows|if_toggles|if_buttons|if_videos)/:if_name/disable_rules/*"
var url_if_hiding_rules =            "/machines/:machine_name/processes/:process_name/:if_kind(if_numbers|if_messages|if_logs|if_arrows|if_toggles|if_buttons|if_videos)/:if_name/hiding_rules/*"
var url_check_invalid_if_name = "/machines/:machine_name/processes/:process_name/:if_kind(if_numbers|if_messages|if_logs|if_arrows|if_toggles|if_buttons|if_videos)/:if_name/*"

var url_machine_disable_rules_get_alias =      "/machines/:machine_name/disable_rules"
var url_machine_hiding_rules_get_alias =       "/machines/:machine_name/hiding_rules"
var url_process_disable_rules_get_alias =      "/machines/:machine_name/processes/:process_name/disable_rules"
var url_process_hiding_rules_get_alias =       "/machines/:machine_name/processes/:process_name/hiding_rules"
var url__if_disable_rules_get_alias =          "/machines/:machine_name/processes/:process_name/:if_kind(if_numbers|if_messages|if_logs|if_arrows|if_toggles|if_buttons|if_videos)/:if_name/disable_rules"
var url_if_hiding_rules_get_alias =            "/machines/:machine_name/processes/:process_name/:if_kind(if_numbers|if_messages|if_logs|if_arrows|if_toggles|if_buttons|if_videos)/:if_name/hiding_rules"
var url_if_data =                         "/machines/:machine_name/processes/:process_name/:if_kind(if_numbers|if_messages|if_logs|if_arrows|if_toggles|if_buttons|if_videos)/:if_name/data"
var url_if_data_signal =                         "/machines/:machine_name/processes/:process_name/:if_kind(if_numbers|if_messages|if_logs|if_arrows|if_toggles|if_buttons|if_videos)/:if_name/data/signal"
var url_if_data_reply =                         "/machines/:machine_name/processes/:process_name/:if_kind(if_numbers|if_messages|if_logs|if_arrows|if_toggles|if_buttons|if_videos)/:if_name/data/reply/:ack_id"
"""
import raspin
api = raspin.api("localhost", 3000)
api.put_machine("test_machine")
api.put_process("computing_resource_logger", "computing resources")
api.processes()
api.put_process("physical_controller", "Physical control")

import random
import time
api.get_process("physical_controller")
api.get_process("computing_resource_logger")
api.put_number_if("cpu", "CPU Usage", 2, "%")
api.put_number_if("memory", "Memory Usage", 2, "%")
r_tgl = api.put_toggle_if("wheel_speed",["fast","middle","slow"], "speed", "physical_controller")
r_move = api.put_arrow_if("wheel_controller", "move", "trbl", "physical_controller")
api.put_arrow_if("arm_sholder", "sholder", "trbl", "physical_controller")
api.put_video_if("Video", "Video", "computing_resource_logger")
api.put_arrow_if("arm_elbow", "elbow", "tb", "physical_controller")
api.ifs("if_numbers")
api.put_data("if_numbers", "cpu", random.randrange(1, 99), "computing_resource_logger")
api.put_data("if_numbers", "memory", random.randrange(1, 99), "computing_resource_logger")

import random
import time


def receive_toggle(data):
    print "toggle:" + str(data)
def receive_arrow(data):
    print "arrow:" + str(data)


api.start_signal_observing("if_arrows", "move", receive_arrow)
api.start_signal_observing("if_toggle", "speed", receive_toggle)
while True:
    api.put_data("if_numbers", "cpu",random.randrange(1,99), "computing_resource_logger")
    api.put_data("if_numbers", "memory",random.randrange(1,99), "computing_resource_logger")
    time.sleep(1)

