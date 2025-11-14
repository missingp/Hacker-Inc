#include "Technology.h"
#include "Virus.h"
#include <iostream>
#include <fstream>
#include "json.hpp"
using json = nlohmann::json;
TechCategory string_to_category(const std::string& s) {
	if (s == "TRANSMISSION")return TechCategory::Transmission;
	if (s == "STEALTH")return TechCategory::STEALTH;
	if (s == "PAYLOAD")return TechCategory::PAYLOAD;
	throw std::runtime_error("Unknown tech category in JSON: " + s);
}
TechTree::TechTree(const std::string& filepath) {
	std::map<std::string, std::function<void(Virus&)>> effect_map;
    effect_map["TRANS_PHISHING"] = [](Virus& v) {
        v.base_spread_chance += 0.1;
        std::cout << "[EFFECT] 基础传播概率提升！\n";
        };
    effect_map["TRANS_USB"] = [](Virus& v) {
        v.has_usb_autorun = true;
        std::cout << "[EFFECT] 已解锁U盘传播能力！\n";
        };
    effect_map["STEALTH_POLY"] = [](Virus& v) {
        v.awareness_factor *= 0.8;
        v.has_polymorphism = true;
        std::cout << "[EFFECT] 警觉度系数降低！\n";
        };
    effect_map["PAYLOAD_BOTNET"] = [](Virus& v) {
        v.can_generate_botnet = true;
        std::cout << "[EFFECT] 已解锁僵尸网络能力！\n";
        };

    std::ifstream file(filepath);
	if (!file.is_open())throw std::runtime_error("Could not open tech tree file: " + filepath);
	json data = json::parse(file);
    for (const auto& tech_json : data["technologies"]) {
        TechNode node;
        node.id = tech_json.at("id").get<std::string>();
        node.name = tech_json.at("name").get<std::string>();
        node.description = tech_json.at("description").get<std::string>();
        node.cost = tech_json.at("cost").get<int>();
        node.category = string_to_category(tech_json.at("category").get<std::string>());
        for (const auto& prereq : tech_json.at("prerequisites")) {
            node.prerequisites.push_back(prereq.get<std::string>());
        }
        if (effect_map.count(node.id)) {
            node.apply_effect = effect_map.at(node.id);
        }
        else {
            // 如果找不到对应的效果，这是一个严重问题，说明数据和代码不匹配
            std::cerr << "[WARNING] No effect defined in C++ for tech ID: " << node.id << std::endl;
            // 可以给一个空效果，防止崩溃
            node.apply_effect = [](Virus& v) {};
        }
		nodes[node.id] = node;
    }
    std::cout << "Tech tree loaded successfully with " << nodes.size() << " technologies.\n\n";
}
TechNode& TechTree::getNode(const std::string& id) {
	return nodes.at(id);
}