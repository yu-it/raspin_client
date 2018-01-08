# -*- coding: utf-8 -*-

import urllib2
import urlparse
import json
import requests
import sseclient
import threading





class api:
    If_Numbers = "if_numbers"
    If_Messages = "if_messages"
    If_Logs = "if_logs"
    If_Arrows = "if_arrows"
    If_Toggles = "if_toggles"
    If_Buttons = "if_buttons"
    If_Video = "if_videos"
    #serverにはサーバ名またはIP,portにはポート番号
    def __init__(self, server, port):
        #http://localhost:3000
        self.api_template = "http://" + server + ":" + str(port) + "/raspin/internal{query}"
        self.current_machine = ""
        self.current_process = ""
        self.current_if = ""
        self.observing = {}
        self.ping()
    def cleansing_uri(self,urlstr):
        return urlstr.replace("//","/").replace("http:/","http://")
    def __api_url(self, path):
        return self.__http_get(self.api_template.format(query = path))
    def __http_get(self, url):
        url = self.cleansing_uri(url)
        self.__log ("get:" + url)
        return self.process_response(requests.get(url))
    def __http_delete(self, url):
        url = self.cleansing_uri(url)
        self.__log ("delete:" + url)
        return self.process_response(requests.delete(url))
    def __http_put(self, url, json_arg = None):
        url = self.cleansing_uri(url)

        self.__log ("put:" + url + ",json:" +  json.dumps(json_arg))
        if (json_arg is None) :
            r = requests.put(url,
                                    headers={'content-type': 'text/plain'},
                                    )
        else:
            r = requests.put(url,json_arg)
        r = self.process_response(r)
        r[1] = url.replace(self.api_template.replace("{query}",""), "")
        r[1] = r[1].replace("?" + urlparse.urlparse(r[1])[4],"")
        return r
    def __log(self, message):
        print(message)
    def process_response(self, r):
        try:
            res = [r.status_code, r.json()]
        except Exception as ex:
            res = [r.status_code, None]
        if res[0] > 300:
            raise Exception("ステータスが{status}".format(), res)
        return res
    def ping(self):
        try:
            ping = self.__http_get(self.api_template.format(query="/ping"))
        except Exception as ex:
            message = "raspin-api 接続エラーが発生しました。" + str(ex)
            self.__log(message)
            raise Exception(message)
    def machines_url(self):
        return self.api_template.format(query="/machines")
    def build_error_message(self, res, url, method):
        return "status:{status}, response:{response}, method:{method}, url:{url}".format(status = res[0],response = res[1],method = method, url=url)
    def machines(self):
        try:
            res = self.__http_get(self.machines_url())
            return res
        except Exception as ex:
            raise Exception(ex)
    def machine_url(self,machine):
        return self.machines_url() + "/" + machine
    def get_machine(self, machine = None):
        if machine is None:
            machine = self.current_machine
        try:
            self.__http_get(self.machine_url(machine))
            self.current_machine = machine
        except Exception as ex:
            raise Exception(ex)
    def put_machine(self, machine = "MyMachine", machine_disp_name = "MyMachine"):
        try:
            r = self.__http_put(self.machine_url(machine) + "?machine_disp_name=" + machine_disp_name)
            self.current_machine = machine
            return r
        except Exception as ex:
            raise Exception(ex)
    def processes_url(self,machine):
        return self.machine_url(machine) + "/processes"
    def processes(self, machine=None):
        if machine is None:
            machine = self.current_machine
        try:
            r = self.__http_get(self.processes_url(machine))
            self.current_machine = machine
            return r
        except Exception as ex:
            raise Exception(ex)
    def process_url(self,machine, process):
        return self.processes_url(machine) + "/" + process
    def get_process(self, process=None, machine=None):
        if process is None:
            process = self.current_process
        if machine is None:
            machine = self.current_machine
        try:
            self.current_machine = machine
            self.current_process = process
            return self.__http_get(self.process_url(machine, process))
        except Exception as ex:
            raise Exception(ex)
    def delete_process(self, process_id, machine = None):
        if machine is None:
            machine = self.current_machine
        try:
            self.current_process = process_id
            return self.__http_delete(self.process_url(machine, process_id))
        except Exception as ex:
            raise Exception(ex)
    def put_process(self, process_id, process_disp_name=None, machine = None):
        if machine is None:
            machine = self.current_machine
        if process_disp_name is None:
            process_disp_name = process_id
        try:
            self.current_process = process_id
            return self.__http_put(self.process_url(machine, process_id) + "?process_disp_name=" + process_disp_name)
        except Exception as ex:
            raise Exception(ex)
    def if_url(self, machine, process, if_kind):
        return self.process_url(machine,process) + "/" + if_kind
    def ifs(self, if_kind, process = None, machine=None):
        if machine is None:
            machine = self.current_machine
        if process is None:
            process = self.current_process
        try:
            self.current_machine = machine
            self.current_process = process
            return self.__http_get(self.if_url(machine, process, if_kind))
        except Exception as ex:
            raise Exception(ex)
    def get_if(self, if_kind, if_id, if_disp_name=None, process = None, machine=None):
        if process is None:
            process = self.current_process
        if machine is None:
            machine = self.current_machine
        if if_disp_name is None:
            if_disp_name = if_id
        try:
            self.current_machine = machine
            self.current_process = process
            return self.__http_get(self.if_url(machine, process, if_kind) + "/" + if_id  + "?if_disp_name=" + if_disp_name)
        except Exception as ex:
            raise Exception(ex)
    def delete_if(self, if_kind, if_id, process=None, machine=None):
        if process is None:
            process = self.current_process
        if machine is None:
            machine = self.current_machine
        try:
            self.current_machine = machine
            self.current_process = process
            return self.__http_delete(self.if_url(machine, process, if_kind) + "/" + if_id )
        except Exception as ex:
            raise Exception(ex)

    def put_if_common_logic(self, if_kind, if_id, json, if_disp_name=None, process=None, machine=None):
        if process is None:
            process = self.current_process
        if machine is None:
            machine = self.current_machine
        if if_disp_name is None:
            if_disp_name = if_id
        try:
            self.current_machine = machine
            self.current_process = process
            return self.__http_put(self.if_url(machine, process, if_kind) + "/" + if_id + "?if_disp_name=" + if_disp_name   , json)
        except Exception as ex:
            raise Exception(ex)
    def put_number_if(self, if_name, if_disp_name=None, scale = 0, unit = "", process=None, machine=None):
        return self.put_if_common_logic(self.If_Numbers, if_name, {"scale": scale, "unit": unit}, if_disp_name, process, machine)
    def put_arrow_if(self, if_name, if_disp_name=None, arrow_state = "tldr", process=None, machine=None):
        return self.put_if_common_logic(self.If_Arrows, if_name, {"enable": arrow_state}, if_disp_name, process, machine)
    def put_video_if(self, if_name, if_disp_name=None, process=None, machine=None):
        return self.put_if_common_logic(self.If_Video, if_name, if_disp_name, process, machine)
    def put_button_if(self, if_name, if_disp_name=None, on_name = "on", off_name = "off", process=None, machine=None):
        return self.put_if_common_logic(self.If_Buttons , if_name, {"on": on_name, "off": off_name}, if_disp_name, process, machine)
    def put_toggle_if(self, if_name, status, if_disp_name=None, process=None, machine=None):
        return self.put_if_common_logic(self.If_Toggles, if_name, {"status": status}, if_disp_name, process, machine)

    def dispatcher_function(self, url, func):
        print "dispatcher start {url}".format(url=url)
        res = sseclient.SSEClient(requests.get(url, stream = True))
        self.observing[threading.current_thread().ident] = res
        try :
            for event in res.events():
                print("get event({url}:{data}".format(url=url,data=str(event)))
                event = json.loads(event.data)
                try:
                    func(event["data"])
                except Exception as ex:
                    print ex
                    pass
                self.__http_put(self.api_template.format(query=event["reply_id"]))
        except Exception as ex:
            self.__log("exception:" + str(ex))
            self.dispatcher_function(url, func)
    def start_signal_observing(self, if_kind, if_id, handler, process=None, machine=None):
        print "observe start {kind} : {id}".format(kind=if_kind, id=if_id)
        if process is None:
            process = self.current_process
        if machine is None:
            machine = self.current_machine
        url = self.if_url(machine,process,if_kind) + "/" + if_id + "/data/signal"
        t = threading.Thread(target=self.dispatcher_function,args = (url, handler))
        t.start()
        return t
    def end_signal_observing(self, t):
        res = self.observing[t.ident]
        res.close()
    def put_data(self, if_kind, if_id, data, process=None, machine=None):
        if process is None:
            process = self.current_process
        if machine is None:
            machine = self.current_machine
        try:
            self.current_machine = machine
            self.current_process = process
            return self.__http_put(self.if_url(machine, process, if_kind) + "/" + if_id + "/data", {"data":data,"data2":data})
        except Exception as ex:
            raise Exception(ex)

