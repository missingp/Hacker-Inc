#pragma once
#include <vector>
#include <string>
#include <iostream>
#include "Country.h"
#include "hacker.h"

class Country;

class NetworkSegment {
public:
	std::string name;
	double securityLevel;
	double infectionRate;
	double awarenessGenerated;
	bool is_controlled;
	std::vector<NetworkSegment*> prerequisities;
	NetworkSegment(std::string n,double security,double awareness):
		name(n),securityLevel(security), awarenessGenerated(awareness), infectionRate(0.0), is_controlled(false) {
	}
	virtual ~NetworkSegment() = default;
	//virtual void update(double deltaTime, Country& owner);
	virtual void apply_control_bonus(Hacker&hacker,Country& owner) = 0;
	virtual void print_status() const {
		std::cout << "  - Segment: " << name << "\n";
		std::cout << "    Security: " << securityLevel << " | Progress: "
			<< (infectionRate * 100.0) << "% | Controlled: "
			<< (is_controlled ? "YES" : "NO") << "\n";
	}
};

// common PC
class CivilianNetwork : public NetworkSegment {
public:
	long long total_hosts;
	long long infected_hosts;
	double hotnet_power;//算力
	double passive_income;//挖矿、广告等被动收益
	//CivilianNetwork(std::string n,long long hosts,double security,double awareness,double power,double income) :
	//	NetworkSegment(n,security, awareness), total_hosts(hosts), infected_hosts(0), hotnet_power(power), passive_income(income) {
	//}
	CivilianNetwork() : NetworkSegment("Civilian PCs", 15.0, 5.0) {}
	void apply_control_bonus(Hacker& hacker,Country& owner) override;
};

class IndustrialNetwork : public NetworkSegment {
public:
	bool can_trigger_sabotage;//是否可以发动破坏行动
	double sabotage_awareness_generated;//破坏行动效果
	//IndustrialNetwork(std::string n,double security, double awareness, bool can_sabotage, double effectiveness) :
	//	NetworkSegment(n,security, awareness), can_trigger_sabotage(can_sabotage), sabotage_awareness_generated(effectiveness) {
	//}
	IndustrialNetwork() : NetworkSegment("Industrial Controls", 70.0, 30.0) {}
	void apply_control_bonus(Hacker&hacker,Country& owner) override;
};

class FinancialNetwork : public NetworkSegment {
public:
	double dailyIncomeOnControl;//控制后每日收益
	bool can_execute_market_crash;//是否可以发动市场崩溃
	//FinancialNetwork(std::string n,double security, double awareness, double income, bool can_crash) :
	//	NetworkSegment(n,security, awareness), dailyIncomeOnControl(income), can_execute_market_crash(can_crash) {
	//}
	FinancialNetwork() : NetworkSegment("Financial System", 85.0, 40.0) {}
	void apply_control_bonus(Hacker& hacker, Country& owner) override;
};

class MediaNetwork : public NetworkSegment {
public:
	double awareness_suppression_factor;//意识抑制系数
	//MediaNetwork(std::string n,double security, double awareness, double suppression) :
	//	NetworkSegment(n,security, awareness), awareness_suppression_factor(suppression) {
	//}
	MediaNetwork() : NetworkSegment("Media Outlets", 50.0, 20.0) {}
	void apply_control_bonus(Hacker& hacker, Country& owner) override;
};

class GovernmentNetwork : public NetworkSegment {
public:
	bool grants_military_access;//是否授予军事访问权限
	//GovernmentNetwork(std::string n,double security, double awareness, bool grants_access) :
	//	NetworkSegment(n,security, awareness), grants_military_access(grants_access) {
	//}
	GovernmentNetwork() : NetworkSegment("Government Network", 90.0, 60.0) {}
	void apply_control_bonus(Hacker& hacker, Country& owner) override;
};

class MilitaryNetwork : public NetworkSegment {
public:
	bool triggers_country_capitulation;//是否触发国家投降
	//MilitaryNetwork(std::string n,double security, double awareness, bool triggers_capitulation) :
	//	NetworkSegment(n,security, awareness), triggers_country_capitulation(triggers_capitulation) {
	//}
	MilitaryNetwork() : NetworkSegment("Military Command", 98.0, 80.0) {}
	void apply_control_bonus(Hacker& hacker, Country& owner) override;
};