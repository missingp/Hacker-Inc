#pragma once
#include <string>
#include <iostream>
#include "Technology.h"
class TechTree;
class Virus {
public:
	int evolution_points;
	//transmission methods
	double base_spread_chance;
	bool has_usb_autorun;
	bool has_0day_exploit;
	//Stealth methods
	double awareness_factor;
	bool has_polymorphism;
	bool has_encryption;
	//Payload methods
	bool can_generate_botnet;
	bool can_use_ransomware;
	bool can_attack_industrial_systems;
private:
	TechTree& tech_tree;
public:
	Virus(TechTree& tree);
	void unlock_tech(const std::string &tech_id);
	void print_status() const;
};