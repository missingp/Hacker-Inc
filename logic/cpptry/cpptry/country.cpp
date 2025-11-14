#include "country.h"
#include "NetworkSegment.h"
#include <iostream>
void GovernmentNetwork::apply_control_bonus(Hacker& hacker, Country& owner) {
    std::cout << "[BONUS] Government network controlled! Military prerequisites cleared.\n";
    // 解锁军事网络的先决条件
    owner.military->prerequisities.clear();
}
Country::Country(const std::string name,double budget,double literacy)
    :name(name),cybersecurity_budget(budget),tech_literacy(literacy){
	civilian = std::make_unique<CivilianNetwork>();
	financial = std::make_unique<FinancialNetwork>();
	industrial = std::make_unique<IndustrialNetwork>();
	military = std::make_unique<MilitaryNetwork>();
	media = std::make_unique<MediaNetwork>();
	government = std::make_unique<GovernmentNetwork>();

    double security_bonus = budget * 0.5; // 假设每点预算提供0.5点安全值
    financial->securityLevel += security_bonus;
    industrial->securityLevel += security_bonus;
    media->securityLevel += security_bonus;
    government->securityLevel += security_bonus;
    military->securityLevel += security_bonus;
    civilian->securityLevel -= (1.0 - literacy) * 10.0;

    financial->prerequisities.push_back(civilian.get());
    // 攻击政府需要先渗透媒体（制造混乱）和金融（获取资源）
    government->prerequisities.push_back(media.get());
    government->prerequisities.push_back(financial.get());
    // 攻击军事的最终堡垒需要先控制政府
    military->prerequisities.push_back(government.get());

    // 4. 填充方便访问的列表
    all_segments = { civilian.get(), financial.get(), industrial.get(), media.get(), government.get(), military.get() };
}

void Country::print_status() const {
    std::cout << "\n===== STATUS REPORT FOR: " << name << " =====\n";
    std::cout << "Cybersecurity Budget: " << cybersecurity_budget
        << " | Population Literacy: " << tech_literacy << "\n";
    for (const auto& segment : all_segments) {
        segment->print_status();
    }
    std::cout << "========================================\n";
}