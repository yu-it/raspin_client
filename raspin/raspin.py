# -*- coding: utf-8 -*-

import urllib2
import json

class api:

    #serverにはサーバ名またはIP,portにはポート番号
    def __init__(self, server, port):
        #http://localhost:3000
        self.api_template = "http://" + server + ":" + str(port) + "/raspin-api/{query}"
        self.ping()

    def __call_api_get(self, path):

        return self.__http_get(self.api_template.format(query = path))

    def __http_get(self, url):
        self.__log (url)
        r = urllib2.urlopen(url)
        res = r.read()
        return json.loads(res)

    def __log(self, message):
        print(message)

    def ping(self):
        try:
            ping = self.__call_api_get("ping")
            self.__log(ping)
        except Exception as ex:
            message = "raspin-api 接続エラーが発生しました。" + str(ex)
            self.__log(message)
            raise Exception(message)

    def subscribe_control_message(self, pvid, timeout_second):
        query = 'SubscribeControlMessage?pvid={pvid}'.format(pvid = pvid)
        try:
            return self.__call_api_get(query)
        except Exception as ex:
            raise ex

    def add_observation_data(self, pvid, data):
        query = 'AddObservationData?pvid={pvid}&data={data}'.format(pvid = pvid, data = urllib2.quote(str(data)))
        self.__call_api_get(query)

    def register_controller_provider_old(self, json_definition):
        return self.regist_controller_provider(json_definition["pvname"], json_definition["queue_size"], json_definition["available_message"]  )

    def register_controller_provider(self, pv_name, queue_size, available_messages,layout_param="default"):
        layout_param=urllib2.quote(layout_param)
        query = "RegisterControllerProvider?pvname={pv_name}&queue_size={queue_size}&layout_param={lay_param}&".format(pv_name=urllib2.quote(pv_name),queue_size=queue_size,lay_param=layout_param)
        msgs = []
        for message in available_messages:
            msgs.append("message_name={message}&arg={arg}".format(message=urllib2.quote(message["message_name"]), arg=message["arg"]))
        query += "&".join(msgs)
        return self.__call_api_get(query)

    def register_data_provider(self,pvname, queue_size, type, unit,layout_param="default"):
        layout_param = urllib2.quote(layout_param)
        query = "RegisterDataProvider?pvname={pv_name}&queue_size={queue_size}&type={type}&unit={unit}&layout_param={lay_param}".format(pv_name=urllib2.quote(pvname),queue_size=queue_size,type=type,unit=unit,lay_param=layout_param)
        return self.__call_api_get(query)

    def mod_controller_provider(self, pvid, pv_name, queue_size, available_messages,layout_param="default"):
        layout_param = urllib2.quote(layout_param)
        query = "ModControllerProvider?pvid={pvid}&pvname={pv_name}&queue_size={queue_size}&layout_param={lay_param}&".format(pvid=pvid,pv_name=urllib2.quote(pv_name),queue_size=queue_size,lay_param=layout_param)
        msgs = []
        for message in available_messages:
            msgs.append("message_name={message}&arg={arg}".format(message=urllib2.quote(message["message_name"]), arg=message["arg"]))
        query += "&".join(msgs)
        return self.__call_api_get(query)

    def acknowledge(self,pvid, req_id, ret, u, d):
        query = "Acknowledge?pvid={pvid}&req_id={reqid}&ret={ret}&".format(pvid=pvid,reqid=req_id,ret=ret)
        umsgs = []
        for update in u:
            umsgs.append("u={u}".format(u=update))

        for de in d:
            umsgs.append("d={d}".format(d=de))
        query += "&".join(umsgs)
        return self.__call_api_get(query)

    def delete_provider(self,pvid):
        query = "DeleteProvider?pvid={pvid}".format(pvid=pvid)
        return self.__call_api_get(query)
