#!/usr/bin/env python3
import argparse
import os
import sys
from time import sleep
import json
from datetime import datetime

import grpc

# Import P4Runtime lib from parent utils dir
# Probably there's a better way of doing this.
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../utils/'))
import p4runtime_lib.bmv2
import p4runtime_lib.helper
from p4runtime_lib.switch import ShutdownAllSwitchConnections
#打开文件
#f = open("/mnt/hgfs/ShareFiles/test.json","rb")

m = 1

def writeTunnelRules(p4info_helper, ingress_sw, egress_sw, tunnel_id,
                                            #定义隧道出入口变量
                     dst_eth_addr, dst_ip_addr,a,b):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.ipv4_lpm",
        match_fields={
            "hdr.ipv4.dstAddr": (dst_ip_addr, 32)
        },
        action_name="MyIngress.myTunnel_ingress",
        action_params={
            "dst_id": tunnel_id,
        })
    ingress_sw.WriteTableEntry(table_entry)
    print("Installed ingress tunnel rule on %s" % ingress_sw.name)

    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.myTunnel_exact",
        match_fields={
            "hdr.myTunnel.dst_id": tunnel_id
        },
        action_name="MyIngress.myTunnel_forward",
        action_params={
            #调用隧道出入口变量
            "port": a
        })
    ingress_sw.WriteTableEntry(table_entry)
    print("Installed transit tunnel rule on %s" % ingress_sw.name)

    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.myTunnel_exact",
        match_fields={
            "hdr.myTunnel.dst_id": tunnel_id
        },
        action_name="MyIngress.myTunnel_egress",
        action_params={
            "dstAddr": dst_eth_addr,
            #调用隧道出入口变量
            "port": b
        })
    egress_sw.WriteTableEntry(table_entry)
    print("Installed egress tunnel rule on %s" % egress_sw.name)


def readTableRules(p4info_helper, sw):

    print('\n----- Reading tables rules for %s -----' % sw.name)
    for response in sw.ReadTableEntries():
        for entity in response.entities:
            entry = entity.table_entry
            # TODO For extra credit, you can use the p4info_helper to translate
            #      the IDs in the entry to names
            table_name = p4info_helper.get_tables_name(entry.table_id)
            print('%s: ' % table_name, end=' ')
            for m in entry.match:
                print(p4info_helper.get_match_field_name(table_name, m.field_id), end=' ')
                print('%r' % (p4info_helper.get_match_field_value(m),), end=' ')
            action = entry.action.action
            action_name = p4info_helper.get_actions_name(action.action_id)
            print('->', action_name, end=' ')
            for p in action.params:
                print(p4info_helper.get_action_param_name(action_name, p.param_id), end=' ')
                print('%r' % p.value, end=' ')
            print()

def printCounter(p4info_helper, sw, counter_name, index, m):

        for response in sw.ReadCounters(p4info_helper.get_counters_id(counter_name), index):
            for entity in response.entities:
                counter = entity.counter_entry
                print("%s %s %d: %d packets (%d bytes)" % (
                    #写入文件
                    sw.name, counter_name, index,

                counter.data.packet_count, counter.data.byte_count)
                )
                print ("内层循环调用中")
                updatejson(sw.name, counter_name, index,
                counter.data.packet_count, counter.data.byte_count, m)


            print("外层循环调用中")

        print("本次函数调用结束")

def printGrpcError(e):
    print("gRPC Error:", e.details(), end=' ')
    status_code = e.code()
    print("(%s)" % status_code.name, end=' ')
    traceback = sys.exc_info()[2]
    print("[%s:%d]" % (traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))

def main(p4info_file_path, bmv2_file_path):
    # Instantiate a P4Runtime helper from the p4info file
    p4info_helper = p4runtime_lib.helper.P4InfoHelper(p4info_file_path)

    try:
        # Create a switch connection object for s1 and s2;
        # this is backed by a P4Runtime gRPC connection.
        # Also, dump all P4Runtime messages sent to switch to given txt files.
        s1 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s1',
            address='127.0.0.1:50051',
            device_id=0,
            proto_dump_file='logs/s1-p4runtime-requests.txt')
        s2 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s2',
            address='127.0.0.1:50052',
            device_id=1,
            proto_dump_file='logs/s2-p4runtime-requests.txt')
        #添加S3交换机信息
        s3 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s3',
            address='127.0.0.1:50053',
            device_id=2,
            proto_dump_file='logs/s3-p4runtime-requests.txt')
        # Send master arbitration update message to establish this controller as
        # master (required by P4Runtime before performing any other write operation)
        s1.MasterArbitrationUpdate()
        s2.MasterArbitrationUpdate()
        s3.MasterArbitrationUpdate()
        #添加S3交换机信息
        # Install the P4 program on the switches
        s1.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_file_path)
        print("Installed P4 Program using SetForwardingPipelineConfig on s1")
        s2.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_file_path)
        print("Installed P4 Program using SetForwardingPipelineConfig on s2")
        #添加S3交换机信息
        s3.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_file_path)
        print("Installed P4 Program using SetForwardingPipelineConfig on s3")
        #定义隧道交换
        writeTunnelRules(p4info_helper, ingress_sw=s1, egress_sw=s2, tunnel_id=100,
                         dst_eth_addr="08:00:00:00:02:22", dst_ip_addr="10.0.2.2",a=2,b=1)
        writeTunnelRules(p4info_helper, ingress_sw=s2, egress_sw=s1, tunnel_id=200,
                         dst_eth_addr="08:00:00:00:01:11", dst_ip_addr="10.0.1.1",a=2,b=1)
        writeTunnelRules(p4info_helper, ingress_sw=s1, egress_sw=s3, tunnel_id=300,
                         dst_eth_addr="08:00:00:00:03:33", dst_ip_addr="10.0.3.3",a=3,b=1)
        writeTunnelRules(p4info_helper, ingress_sw=s3, egress_sw=s1, tunnel_id=400,
                         dst_eth_addr="08:00:00:00:01:11", dst_ip_addr="10.0.1.1",a=2,b=1)
        writeTunnelRules(p4info_helper, ingress_sw=s2, egress_sw=s3, tunnel_id=500,
                         dst_eth_addr="08:00:00:00:03:33", dst_ip_addr="10.0.3.3",a=3,b=1)
        writeTunnelRules(p4info_helper, ingress_sw=s3, egress_sw=s2, tunnel_id=600,
                         dst_eth_addr="08:00:00:00:02:22", dst_ip_addr="10.0.2.2",a=3,b=1)
        #读取
        readTableRules(p4info_helper, s1)
        readTableRules(p4info_helper, s2)
        readTableRules(p4info_helper, s3)
        #打印
        while True:
            sleep(2)
            print('\n----- Reading tunnel counters -----')
            m = 1
            a = datetime.now()
            printCounter(p4info_helper, s1, "MyIngress.ingressTunnelCounter", 100, m)

            print(a)
            m = m + 1
            printCounter(p4info_helper, s2, "MyIngress.egressTunnelCounter", 100, m)
            m = m + 1

            print(a)
            printCounter(p4info_helper, s2, "MyIngress.ingressTunnelCounter", 200, m)
            m = m + 1

            print(a)
            printCounter(p4info_helper, s1, "MyIngress.egressTunnelCounter", 200, m)
            m = m + 1

            print(a)
            printCounter(p4info_helper, s1, "MyIngress.ingressTunnelCounter", 300, m)
            m = m + 1

            printCounter(p4info_helper, s3, "MyIngress.egressTunnelCounter", 300, m)
            m = m + 1

            printCounter(p4info_helper, s3, "MyIngress.ingressTunnelCounter", 400, m)
            m = m + 1

            printCounter(p4info_helper, s1, "MyIngress.egressTunnelCounter", 400, m)
            m = m + 1

            printCounter(p4info_helper, s2, "MyIngress.ingressTunnelCounter", 500, m)
            m = m + 1

            printCounter(p4info_helper, s3, "MyIngress.egressTunnelCounter", 500, m)
            m = m + 1

            printCounter(p4info_helper, s3, "MyIngress.ingressTunnelCounter", 600, m)
            m = m + 1

            printCounter(p4info_helper, s2, "MyIngress.egressTunnelCounter", 600, m)
            gettime("h1","2",1,2)
            gettime("h2","1",3,4)
            gettime("h2","3",5,6)
            gettime("h3","2",7,8)
            gettime("h1","3",9,10)
            gettime("h3","1",11,12)
    except KeyboardInterrupt:
        print("你刚才摁了CTRL + C对吧")
    except grpc.RpcError as e:
        printGrpcError(e)

    ShutdownAllSwitchConnections()

# 获取json里面数据
def get_json_data(sw_name, counter_name, index,
                counter_data_packet_count, counter_data_byte_count, m):
      m_index = str(m)
      with open("/media/sf_share/test.json", 'rb') as f:# 使用只读模型，并定义名称为f
        params = json.load(f)  # 加载json文件
        params[m_index]["sw.name"] = sw_name  # code字段对应的值修改为404
        params[m_index]["counter_name"] = counter_name
        params[m_index]["index"] = index
        params[m_index]["counter.data.byte_count"] = counter_data_byte_count
        params[m_index]["counter.data.packet_count"] = str(counter_data_packet_count)
        print("params", params)  # 打印
      return params
    # 返回修改后的内容


# 写入json文件
def write_json_data(params):
    # 使用写模式，名称定义为r
    #其中路径如果和读json方法中的名称不一致，会重新创建一个名称为该方法中写的文件名
    with open("/media/sf_share/test.json", 'w') as r:
        # 将dict写入名称为r的文件中
        json.dump(params, r)


# 调用两个函数，更新内容
def updatejson(sw_name, counter_name, index,
                counter_data_packet_count, counter_data_byte_count, m):
    the_revised_dict = get_json_data(sw_name, counter_name, index,
                counter_data_packet_count, counter_data_byte_count, m)
    write_json_data(the_revised_dict)
# def gettime():
#     a = datetime.()
#     def gettimebetween():
def gettime(hname,addr,id_one,id_two):
    #通过iperf检测并保存结果
    re = os.popen(F"mx {hname} iperf -u -c 10.0.{addr}.{addr} -b 900M  -i 1  -w 1M  -t 2").readlines()
    result = []
    m_index1 = str(id_one)
    m_index2 = str(id_two)
    print("即将开始循环")
    for i in range(0, len(re) - 1):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
        res = re[i].strip('\n')
        print(str(res))
        result.append(res)
        print(str(len(result)))
    myresult = str(result[len(result)-1])
    #打印的是
    print(myresult)
    print("这是一行")
    print(str(result[len(result)-1]))
    jsonresult = str(result[len(result)-1])
    jsonresultlist = jsonresult.split()
    print(jsonresultlist[5])
    with open("/media/sf_share/test.json", 'rb') as f:# 使用只读模型，并定义名称为f
        params = json.load(f)  # 加载json文件
        params[m_index1]["transfer"] = jsonresultlist[5]
        params[m_index1]["bandwidth"] = jsonresultlist[7]
        params[m_index2]["transfer"] = jsonresultlist[5]
        params[m_index2]["bandwidth"] = jsonresultlist[7]  # code字段对应的值修改为404
    with open("/media/sf_share/test.json", 'w') as r:
        # 将dict写入名称为r的文件中
        json.dump(params, r)
    print(jsonresultlist[7])
    print("打印结果中\n\n\n\n\n\n\n\n\n\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P4Runtime Controller')
    parser.add_argument('--p4info', help='p4info proto in text format from p4c',
                        type=str, action="store", required=False,
                        default='./build/advanced_tunnel.p4.p4info.txt')
    parser.add_argument('--bmv2-json', help='BMv2 JSON file from p4c',
                        type=str, action="store", required=False,
                        default='./build/advanced_tunnel.json')
    args = parser.parse_args()

    if not os.path.exists(args.p4info):
        parser.print_help()
        print("\np4info file not found: %s\nHave you run 'make'?" % args.p4info)
        parser.exit(1)
    if not os.path.exists(args.bmv2_json):
        parser.print_help()
        print("\nBMv2 JSON file not found: %s\nHave you run 'make'?" % args.bmv2_json)
        parser.exit(1)
    main(args.p4info, args.bmv2_json)

    m = 1
