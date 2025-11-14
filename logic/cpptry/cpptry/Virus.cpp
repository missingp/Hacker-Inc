#include "Virus.h"
#include "Technology.h"
Virus::Virus(TechTree&tree):tech_tree(tree){
	evolution_points = 50;
	base_spread_chance = 0.05;
	has_usb_autorun = false;
	has_0day_exploit - false;
	awareness_factor = 1.0;
	has_polymorphism = false;
	has_encryption = false;
	can_generate_botnet = false;
	can_use_ransomware = false;
	can_attack_industrial_systems = false;
}

void Virus::unlock_tech(const std::string& tech_id) {
	TechNode& node = tech_tree.getNode(tech_id);
	if (node.is_unlocked) {
		std::cout << "[FAIL] 科技 '" << node.name << "' 已经解锁。\n";
		return;
	}
	if (evolution_points < node.cost) {
		std::cout << "[FAIL] EP不足! 需要 " << node.cost << ", 你只有 " << evolution_points << "。\n";
		return;
	}
	for (const std::string& prereq_id : node.prerequisites) {
		if (!tech_tree.getNode(prereq_id).is_unlocked) {
			std::cout << "[FAIL] 前置科技 '" << tech_tree.getNode(prereq_id).name << "'尚未解锁。\n";
			return;
		}
	}
	evolution_points -= node.cost;
	node.apply_effect(*this); // 调用lambda函数，修改自身属性
	node.is_unlocked = true;

	std::cout << "[SUCCESS] 成功解锁科技 '" << node.name << "'! 剩余EP: " << evolution_points << "\n\n";
}
void Virus::print_status()const {
	std::cout << "========== VIRUS STATUS ==========\n";
	std::cout << "Evolution Points: " << evolution_points << "\n";
	std::cout << "Spread Chance: " << base_spread_chance << "\n";
	std::cout << "Awareness Factor: " << awareness_factor << "\n";
	std::cout << "USB Spread Unlocked: " << (has_usb_autorun ? "Yes" : "No") << "\n";
	std::cout << "Botnet Unlocked: " << (can_generate_botnet ? "Yes" : "No") << "\n";
	std::cout << "================================\n\n";
}