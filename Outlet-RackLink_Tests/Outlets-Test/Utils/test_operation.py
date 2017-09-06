"""
These functions handle functionality including but not limited to:
 - tests' operations
 - repetitive tasks
 - repetitive commands

"""


def ip_baseUrl_title(baseUrl):
    print "\n\nTesting on IP Address: " + baseUrl
    print "\n--------------------------------------------"


def outlet_count(count):
    print "\n::::: Outlet " + str(count) + " :::::\n"


def get_ip_addresses():
    inFile = open(".\\test_ip_addresses.txt", "r")
    lines = inFile.readlines()
    inFile.close()

    all_ips = []

    for line in lines:
        words = [x.strip() for x in line.split(',')]
        for word in words:
            if word == '':
                continue
            all_ips.append(word)
    return all_ips


def ip_nodes(ipNumVal):
    nodes = ipNumVal.split(".")
    return nodes


def host_nodes(ipNumVal):
    nodes = ipNumVal.split(".")

    charNodes = []

    for node in nodes:
        if not node.isdigit():
            charNodes.append(node)

    return charNodes

def starts_with_zero(ipNumVal, ipInputClass):
    if ipNumVal[0] == "0":
        if 'has-error' in ipInputClass:
            return True
        else:
            return False


def ends_with_zero(ipNumVal, ipInputClass):
    if ipNumVal[-1] == "0":
        if 'has-error' in ipInputClass:
            return True
        else:
            return False


def node_255(ipNumVal, ipInputClass):
    nodes = ip_nodes(ipNumVal)

    for node in nodes:
        intNode = int(node)
        if intNode >= 255:
            if 'has-error' in ipInputClass:
                return True
            else:
                return False


def short_ip_node_length(ipNumVal, ipInputClass):
    nodes = ip_nodes(ipNumVal)

    if len(nodes) < 4:
        if 'has-error' in ipInputClass:
            return True
        else:
            return False


def short_host_node_length(ipNumVal, ipInputClass):
    nodes = host_nodes(ipNumVal)

    if len(nodes) < 3:
        if 'has-error' in ipInputClass:
            return True
        else:
            return False


def long_ip_node_length(ipNumVal, ipInputClass):
    nodes = ip_nodes(ipNumVal)

    if len(nodes) > 4:
        if 'has-error' in ipInputClass:
            return True
        else:
            return False
