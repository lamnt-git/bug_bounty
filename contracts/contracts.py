from web3 import Web3, HTTPProvider
from solcx import compile_source, compile_files

class Contract(object):
    def __init__(self, _address, _contract_file="contracts/BugBounty.sol"):
        self.HOST                    = "172.31.160.1"
        self.PORT                    = 8545
        self.web3                    = Web3(HTTPProvider('http://%s:%d' % (self.HOST, self.PORT)))
        self.contract_file           = _contract_file
        self.web3.eth.defaultAccount = _address


    def compile_contract(self):
        data     = open(self.contract_file, "r").read()
        contract = compile_source(data)

        for key in contract.keys():
            self.contract = contract[key]

        self.abi = self.contract['abi']
        self.bin = self.contract['bin']

    def construct(self, baseBounty, scope, notice):
        self.compile_contract()
        eth_contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bin)
        self.eth_contract = eth_contract.constructor(baseBounty, ",".join(scope), notice)

    def deploy(self):
        txtHash = self.eth_contract.transact()
        self.contractAddress = self.web3.eth.waitForTransactionReceipt(txtHash)['contractAddress']
        return self.contractAddress


class HackerInterface(object):
    def __init__(self, _address):
        self.HOST                    = "172.31.160.1"
        self.PORT                    = 8545
        self.web3                    = Web3(HTTPProvider('http://%s:%d' % (self.HOST, self.PORT)))
        self.address                 = _address
        self.web3.eth.defaultAccount = _address

    def submitBug(self, _name, _severity, _contractAddr, _contractAbi):
        if _severity == "LOW":
            severity = 4
        elif _severity == "MEDIUM":
            severity = 5
        elif _severity == "HIGH":
            severity = 6
        elif _severity == "CRITICAL":
            severity = 7
        else:
            return False

        contract = self.web3.eth.contract(address=_contractAddr, abi=_contractAbi)
        f = contract.functions.submitBug(_name, severity)
        print(f.estimateGas())
        txtHash = f.transact({'from': self.address, 'gas': 300000})
        receipt = self.web3.eth.waitForTransactionReceipt(txtHash)
        
        submissionId = contract.functions.getCurrentId().call()

        return submissionId

    def getContractStatus(self, _contractAddr, _contractAbi):
        contract = self.web3.eth.contract(address=_contractAddr, abi=_contractAbi)
        isProcessing = contract.functions.getState().call()

        if isProcessing is True:
            return "Busy"
        return "Free"

class CompanyInterface(object):
    def __init__(self, _address):
        self.HOST                    = "172.31.160.1"
        self.PORT                    = 8545
        self.web3                    = Web3(HTTPProvider('http://%s:%d' % (self.HOST, self.PORT)))
        self.address                 = _address
        self.web3.eth.defaultAccount = _address

    def rewardBounty(self, _bounty, _comment, _contractAddr, _contractAbi):
        contract = self.web3.eth.contract(address=_contractAddr, abi=_contractAbi)
        f = contract.functions.processSubmission(1, _bounty, _comment)

        txtHash = f.transact({'from': self.address, 'gas': 300000})
        receipt = self.web3.eth.waitForTransactionReceipt(txtHash)


    def rejectSubmission(self, _comment, _contractAddr, _contractAbi):
        contract = self.web3.eth.contract(address=_contractAddr, abi=_contractAbi)
        f = contract.functions.processSubmission(2, 0, _comment)

        txtHash = f.transact({'from': self.address, 'gas': 300000})
        receipt = self.web3.eth.waitForTransactionReceipt(txtHash)


    def topUpContract(self, _contractAddr, _amount):
        txtHash = self.web3.eth.sendTransaction({'to': _contractAddr, 'from': self.address, 'value': _amount * (10 ** 9)})
        receipt = self.web3.eth.waitForTransactionReceipt(txtHash)
        print(receipt)
