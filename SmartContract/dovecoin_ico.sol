// DoveCoin ICO


//Versión del Compilador
pragma solidity ^0.8.27;

contract dovecoin_ico {

    //====Variables Pública====

    //Num max de dovecoin para comprar (100M):
    uint128 public max_dovecoins = 100000000;

    // Ratio conversión  Dovecoin - dólars (1$ = 1000 dovecoin)
    uint public usd_to_dovecoins = 1000;

    // Número total de DoveCoins compradas por inversores
    uint public total_dovecoins_bought = 0;

    //Mapping que dada la direcc del inversión, devuelve su equite tanto en DoveCoins como en USD
    mapping(address => uint) equity_dovecoins; //Para cada dirección, devuelve el balance en DoveCoin
    mapping(address => uint) equity_usd;       // Equity del inversor pero en USD

    //MOdificador: controlar si una operación se puede o no llevar a cabo
    // Comprobar si el inversor puede comprar tantas dovecoins como quiere
    modifier can_buy_dovecoin(uint usd_invested) {
        uint dovecoin_left = max_dovecoins - total_dovecoins_bought;
        require(usd_invested * usd_to_dovecoins <= dovecoin_left, "Not enough Dovecoin left to buy.");
        _; // Ejecutar una función (se ponen antes de una función para comprobar que hay suficientes dovecoins)
    }

    //Obtener el balance de DoveCoin de un Inversor
    function equity_in_dovecoins(address addr_investor) external view returns (uint) {//constante externa, fuera del contrato
        return equity_dovecoins[addr_investor];
    }

    //Obtener el balance de USD de un Inversor
    function equity_in_usd(address addr_investor) external view returns (uint) {//constante externa, fuera del contrato
        return equity_usd[addr_investor];
    }

    // Actualizar equity en dovecoins y en usd + dovecoins compradas despúes de que el inversión compre
    // Comprar DoveCoins, antes de preparar el cuerpo de la función hay que usar el modificador
    function buy_dovecoins(address addr_investor, uint usd_invested) external
    can_buy_dovecoin(usd_invested){
        uint dovecoin_bought = usd_invested * usd_to_dovecoins;
        equity_dovecoins[addr_investor]+= dovecoin_bought; //vemos la cantidad
        equity_usd[addr_investor] += usd_invested;
        total_dovecoins_bought += dovecoin_bought;
    }

    // Devolver el dinero
    function sell_dovecoins(address addr_investor, uint dovecoins_sold) external {
        equity_dovecoins[addr_investor]-= dovecoins_sold; //vemos la cantidad
        uint usd_sold = dovecoins_sold / usd_to_dovecoins;
        equity_usd[addr_investor] -= usd_sold;
        total_dovecoins_bought -= dovecoins_sold;
    }


}