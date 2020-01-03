from web3 import Web3, HTTPProvider
from solcx import compile_source, compile_files

class Contract(object):
    def __init__(self, _contract_file="contracts/BugBounty.sol"):
        self.HOST          = "172.31.160.1"
        self.PORT          = 8545
        self.web3          = Web3(HTTPProvider('http://%s:%d' % (self.HOST, self.PORT)))
        self.contract_file = _contract_file


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
        return eth_contract.constructor(baseBounty, ",".join(scope), notice)