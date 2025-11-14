#pragma once
#include <memory>
#include <string>
#include "NetworkSegment.h"
class CivilianNetwork;
class FinancialNetwork;
class IndustrialNetwork;
class MediaNetwork;
class GovernmentNetwork;
class MilitaryNetwork;
class NetworkSegment;
class Country {
public:
	std::string name;
	double cybersecurity_budget;
	double tech_literacy;
	double awareness_modifier = 1.0;
	std::unique_ptr<CivilianNetwork>civilian;
	std::unique_ptr<IndustrialNetwork>industrial;
	std::unique_ptr<MediaNetwork>media;
	std::unique_ptr<FinancialNetwork>financial;
	std::unique_ptr<GovernmentNetwork>government;
	std::unique_ptr<MilitaryNetwork>military;
	std::vector<NetworkSegment*> all_segments;
	Country(const std::string name, double budget, double literacy);
	void update(double deltaTime);
	void print_status()const;
};