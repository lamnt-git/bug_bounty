
pragma solidity ^0.5.0;


/// @title BugBounty
contract BugBounty {

    event NewProgram(uint baseBounty, string scope, string notice);
    event Deposit(address indexed sender, uint value);
    event ProgramChanged(uint baseBounty, string scope, string notice);
    event NewSubmission(address indexed submiter, string name, uint indexed submissionId);
    event RewardBounty(address indexed hacker, string name, uint bounty, string comment);
    event RejectSubmission(address indexed hacker, string name, string comment);


    /*
     *  Constants
     */

    uint constant ACCEPT = 1;
    uint constant REJECT = 2;

    uint LOW = 4;
    uint MEDIUM = 5;
    uint HIGH = 6;
    uint CRITICAL = 7;


    address owner;
    uint public baseBounty;
    string public scope;
    string public notice;
    uint public submissionCount;

    Submission currentSubmission;
    bool isProcessing;

    struct Submission {
        address payable hacker;
        string name;
        uint severity;
        uint bounty;
        uint submissionId;
    }


    modifier validRequirement(uint _baseBounty) {
        // require(ownerCount <= MAX_OWNER_COUNT
        //     && _required <= ownerCount
        //     && _required != 0
        //     && ownerCount != 0);
        // _;
        require(_baseBounty > 0);
        _;
    }

    modifier isFree() {
        require(isProcessing == false);
        _;
    }

    modifier isBusy() {
        require(isProcessing == true);
        _;
    }

    modifier isOwner(address addr) {
        require(addr == owner);
        _;
    }

    modifier isValidBounty(uint _bounty) {
        require(_bounty > 0);
        _;
    }


    /// @dev Fallback function allows to deposit ether.
    function()
        payable external
    {
        if (msg.value > 0)
            emit Deposit(msg.sender, msg.value);
    }

    /*
     * Public functions
     */
    constructor(uint _baseBounty, string memory _scope, string memory _notice)
        public
        validRequirement(_baseBounty)
    {
        owner = msg.sender;

        baseBounty = _baseBounty;
        scope     = _scope;
        notice    = _notice;

        submissionCount = 0;
        isProcessing    = false;
        emit NewProgram(baseBounty, scope, notice);
    }


    function changeProgram(uint _baseBounty, string memory _scope, string memory _notice)
        public
        isFree()
        isOwner(msg.sender)
        validRequirement(_baseBounty)
    {
        baseBounty = _baseBounty;
        scope     = _scope;
        notice    = _notice;
        emit ProgramChanged(_baseBounty, _scope, _notice);
    }


    function getState()
        public
        view
        returns (bool) 
    {
        if (isProcessing) {
            return true;
        }
        return false;
    }


    function getCurrentId()
        public
        view
        returns (uint)
    {
        return currentSubmission.submissionId;
    }


    function submitBug(string memory _name, uint _severity)
        public
        isFree()
        returns (uint submissionId)
    {
        submissionId = submissionCount;

        currentSubmission = Submission({
            hacker      : address(uint160(msg.sender)),
            name        : _name,
            severity    : _severity,
            bounty      : 0,
            submissionId: submissionCount
        });

        isProcessing = true;
        submissionCount += 1;

        emit NewSubmission(currentSubmission.hacker, currentSubmission.name, currentSubmission.submissionId);
    }


    function processSubmission(uint _action, uint _bounty, string memory _comment)
    public
    isOwner(msg.sender)
    isBusy()
    {
        if (_action == ACCEPT) {
            rewardBounty(currentSubmission.hacker, _bounty);
            emit RewardBounty(currentSubmission.hacker, currentSubmission.name, currentSubmission.bounty, _comment);
        }
        if (_action == REJECT) {
            emit RejectSubmission(currentSubmission.hacker, currentSubmission.name, _comment);
        }
        isProcessing = false;
    }


    function rewardBounty(address payable _addr, uint _bounty)
    private
    isValidBounty(_bounty)
    {
        currentSubmission.bounty = _bounty;
        sendCoin(_addr, _bounty);
    }

    function sendCoin(address payable addr, uint bounty)
    private
    {
        addr.transfer(bounty);
    }
}
