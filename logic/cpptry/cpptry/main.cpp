#include "Technology.h"
#include "Virus.h"
#include<vector>
#include <string>
#include <iostream>
#include "country.h"
#include "hacker.h"

void simulate_attack(NetworkSegment& target, Hacker& hacker, Country& country) {
	std::cout<<"\n>>> Simulating attack on: " << target.name << " <<<\n";
    if (target.is_controlled) {
        std::cout << "[FAIL] Target is already controlled.\n";
        return;
    }

    for (const auto& prereq : target.prerequisities) {
        if (!prereq->is_controlled) {
            std::cout << "[FAIL] Prerequisite not met: Must control '" << prereq->name << "' first.\n";
            return;
        }
    }

    double progress_this_turn = hacker.botnet_power / target.securityLevel;
    target.infectionRate += progress_this_turn;

    std::cout << "[INFO] Attack progress this turn: " << (progress_this_turn * 100.0) << "%\n";

    if (target.infectionRate >= 1.0) {
        target.infectionRate = 1.0;
        target.is_controlled = true;
        std::cout << "[SUCCESS] Target '" << target.name << "' has been fully controlled!\n";
        target.apply_control_bonus(hacker, country); // 应用奖励
    }
}

void print_hacker_status(const Hacker& hacker) {
    std::cout << "\n--- HACKER STATUS ---\n";
    std::cout << "Money: $" << hacker.money << "\n";
    std::cout << "Botnet Power: " << hacker.botnet_power << "\n";
    std::cout << "---------------------\n";
}

int main() {
    Hacker player;
    Country test_country("Switzerland", 80.0, 0.95); // 一个高难度国家

    print_hacker_status(player);
    test_country.print_status();

    // 模拟游戏进程
    std::cout << "\n--- TURN 1: Attacking Military first (should fail) ---\n";
    simulate_attack(*test_country.military, player, test_country);

    std::cout << "\n--- TURN 2: Attacking Civilian network (should be easy) ---\n";
    simulate_attack(*test_country.civilian, player, test_country);

    std::cout << "\n--- TURN 3: Attacking Civilian network again... ---\n";
    //simulate_attack(*test_country.civilian, player, test_country); // 应该很快就能控制住
    for (int i = 0; i < 20; ++i) {
        if (!test_country.financial->is_controlled) {
            simulate_attack(*test_country.civilian, player, test_country);
        }
    }
    print_hacker_status(player); // 检查僵尸网络算力是否增加
    test_country.print_status();

    std::cout << "\n--- TURN 4: Attacking Financial network (should fail, needs Civilian) ---\n";
    // 噢，等等，我们的逻辑是控制后才能攻击下一个，所以现在应该可以攻击了
    // 让我们攻击4轮看看进展
    std::cout << "\n--- TURNS 4-7: Sustained attack on Financial network ---\n";
    for (int i = 0; i < 4; ++i) {
        if (!test_country.financial->is_controlled) {
            simulate_attack(*test_country.financial, player, test_country);
        }
    }
    test_country.print_status();
    print_hacker_status(player); // 检查钱是否增加

    std::cout << "\n--- FINAL TEST: Now that we control Civilian, we can attack Financial ---\n";
    // 为了演示，我们假设玩家已经控制了所有前置，直接攻击军事
    std::cout << "\n--- Let's pretend we control everything else and attack the Military ---\n";
    test_country.government->is_controlled = true; // 手动作弊以测试
    test_country.government->prerequisities.clear(); // 清除先决条件
    test_country.military->prerequisities.clear();   // 清除先决条件
    for (int i = 0; i < 5; ++i) { // 军事网络非常难攻
        simulate_attack(*test_country.military, player, test_country);
    }
    test_country.print_status();
    print_hacker_status(player);
    return 0;
}
//try {
//	TechTree techtree("tech_tree.json");
//	Virus my_virus(techtree);
//       std::cout << "游戏开始！\n";
//       my_virus.print_status();

//       // 后续的逻辑完全不需要改变！
//       std::cout << ">>> 尝试解锁 'U盘感染' (前置条件未满足)...\n";
//       my_virus.unlock_tech("TRANS_USB");
//       my_virus.print_status();

//       std::cout << ">>> 尝试解锁 '钓鱼邮件'...\n";
//       my_virus.unlock_tech("TRANS_PHISHING");
//       my_virus.print_status();

//       std::cout << ">>> 再次尝试解锁 'U盘感染'...\n";
//       my_virus.unlock_tech("TRANS_USB");
//       my_virus.print_status();
   //}
//   catch (const std::exception& e) {
//       std::cerr << "An error occurred: " << e.what() << std::endl;
//       return 1;
//   }