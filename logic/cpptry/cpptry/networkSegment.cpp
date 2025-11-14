#include "NetworkSegment.h"
#include <iostream>
void CivilianNetwork::apply_control_bonus(Hacker& hacker, Country& owner) {
    std::cout << "[BONUS] Civilian network controlled! Gained +20 Botnet Power.\n";
    hacker.botnet_power += 20.0;
}

void FinancialNetwork::apply_control_bonus(Hacker& hacker, Country& owner) {
    std::cout << "[BONUS] Financial system controlled! Gained $50,000.\n";
    hacker.money += 50000.0;
}

void IndustrialNetwork::apply_control_bonus(Hacker& hacker, Country& owner)  {
    std::cout << "[BONUS] Industrial network controlled! Physical sabotage is now possible.\n";
}

void MediaNetwork::apply_control_bonus(Hacker& hacker, Country& owner)  {
    std::cout << "[BONUS] Media controlled! Future awareness generation in this country is reduced.\n";
    // 假设Country类有一个awareness_modifier属性
    owner.awareness_modifier *= 0.75;
}

void MilitaryNetwork::apply_control_bonus(Hacker& hacker, Country& owner)  {
    std::cout << "\n**************************************************\n";
    std::cout << "[VICTORY] MILITARY CONTROLLED! " << owner.name << " is yours!\n";
    std::cout << "**************************************************\n";
}
