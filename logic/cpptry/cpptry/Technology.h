#pragma once
#include <string>
#include <vector>
#include <functional>
#include <map>
#include "Virus.h"
class Virus;
enum class TechCategory {
	Transmission,
	STEALTH,
	PAYLOAD
};

struct TechNode {
	std::string id;
	std::string name;
	std::string description;
	TechCategory category;
	int cost;
	std::vector<std::string> prerequisites;
	bool is_unlocked;
	std::function<void(Virus&)> apply_effect;
};
class TechTree {
public:
	std::map<std::string, TechNode> nodes;
	TechTree(const std::string &filepath);
	TechNode& getNode(const std::string& id);
};