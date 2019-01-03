//Kartcoins ICO

pragma solidity ^0.5.2;

contract kartcoin_ico{
    
    //Introducing maximum number of kartcoin available for seale
    uint public max_kartcoin= 1000000;
    
    //Introducing USD to kartcoin conversion
    uint public usd_to_kartcoin=1000;
    
    //total number of kartcoin bought ffrom investors
    uint public total_kartcoin_bought=0;
    
    //mapping from investors side equity of kartcoin and USD
    mapping(address=> uint) equity_kartcoins;
    mapping(address=> uint) equity_usd;
    
    //modifier to check wheather the investor can buy coins or not

    modifier can_buy_kartcoins(uint usd_invested){
        require(usd_invested*usd_to_kartcoin+total_kartcoin_bought <=max_kartcoin);
        _;
    }
    
    //Getting the equity in Kartcoin of an investor
    
    function equity_in_kartcoin(address investor) external view returns(uint){
        return equity_kartcoins[investor];
    }
    
     //Getting the equity in USD of an investor
    
    function equity_in_usd(address investor) external view returns(uint){
        return equity_usd[investor];
    }
    
    //Buying Kartcoin
    function buy_kartcoins(address investor,uint usd_invested) external
    can_buy_kartcoins(usd_invested){
        uint kartcoin_bought = usd_invested*usd_to_kartcoin;
        equity_kartcoins[investor]+=kartcoin_bought;
        equity_usd[investor]+= equity_kartcoins[investor]/1000;
        total_kartcoin_bought=kartcoin_bought;
    }
    
    
    
    
    
    
    
    
    
    

}

