import random
import copy
from collections import defaultdict
from datetime import datetime, timedelta

class Pet:
    def __init__(self, name, pet_type):
        self.name = name
        self.type = pet_type
        self.level = 1
        self.exp = 0
        self.hunger = 0
        self.evolution = 0 
        
    def feed(self):
        self.hunger = 0
        return True
    
    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= 200:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.exp -= 200
        print(f"{self.name}升级到了{self.level}级！")

class Player:
    def __init__(self):
        self.health = 100
        self.max_health = 100
        self.stamina = 100
        self.max_stamina = 100
        self.energy = 80  
        self.max_energy = 100
        self.day = 1
        self.exp = 0
        self.level = 1
        self.last_eaten = datetime.now()
        self.health_points = 30  
        self.consecutive_healthy_days = 0
        
        self.sword_level = 1
        self.armor_level = 1
        self.passive_skills = defaultdict(int)  
        
        self.inventory = defaultdict(int)
        self.inventory.update({
            '石头': 0,
            '木头': 0,
            '纤维': 0,
            '钥匙': 0,
            '盐': 0,
            '生肉': 0,
            '熏肉': 0,
            '鱼': 0,
            '熏鱼': 0,
            '兽皮': 0,
            '水晶': 0,
            '草药': 0,
            '药膏': 0
        })
        
        self.pets = []
        self.active_pets = []
        self.pet_evolution = defaultdict(int)
        self.food_expiry = {}
        self.unlocked_secret = False
        self.unlocked_ship = False
        self.monster_skills = defaultdict(int)
    def check_pet_hunger(self):
        """检查所有活跃宠物饥饿状态，返回是否有宠物过于饥饿"""
        hungry_pets = [pet for pet in self.active_pets if pet.hunger >= 10]
        for pet in hungry_pets:
            print(f"\n警告：{pet.name}({pet.type})非常饥饿！饥饿度: {pet.hunger}/10")
        return len(hungry_pets) == 0  
    def show_status(self):
        print(f"\n============== 第{self.day}天 ==============")
        print(f"生命: {self.health}/{self.max_health} | 体力: {self.stamina}/{self.max_stamina}")
        print(f"精力: {self.energy}/{self.max_energy} | 健康值: {self.health_points}/50")
        print(f"等级: {self.level} (经验: {self.exp}/200")
        print(f"武器: Lv{self.sword_level} | 护甲: Lv{self.armor_level}")
    
        if self.passive_skills:
            print("被动技能:")
            for skill, level in self.passive_skills.items():
                print(f"  {skill} Lv{level}", end=" | ")
            print()
    
        if self.monster_skills:
            print("怪物技能:")
            for skill, level in self.monster_skills.items():
                print(f"  {skill} Lv{level}", end=" | ")
            print()
    
        if self.active_pets:
            print("携带宠物:")
            for i, pet in enumerate(self.active_pets, 1):
                print(f"  {i}. {pet.name} ({pet.type}, Lv{pet.level}, 饥饿度: {pet.hunger}/10)")
    
        print("\n资源:")
        for item, count in self.inventory.items():
            if count > 0:  # 只显示数量大于0的资源
                print(f"  {item}: {count}", end=" | ")
        print()

       
    
        print("\n\n当前进度:")
        if self.unlocked_ship:
            print("已解锁造船技术")
        elif self.unlocked_secret:
            print("已发现岛屿秘密")
        
    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= 200:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.exp -= 200
        prev_max_health = self.max_health
        prev_max_stamina = self.max_stamina
        prev_max_energy = self.max_energy
        
        self.max_health += 10
        self.max_stamina += 2
        self.max_energy += 2
        
        print(f"\n=== 升级到 {self.level} 级! ===")
        print(f"最大生命值 {prev_max_health} → {self.max_health}")
        print(f"最大体力值 {prev_max_stamina} → {self.max_stamina}")
        print(f"最大精力值 {prev_max_energy} → {self.max_energy}")
        
        # 提供技能选择
        skill_options = [
            "生命恢复+", "暴击率+", 
            "采集效率+", "战斗经验+"
        ]
        
        print("\n选择一个新技能:")
        for i, skill in enumerate(skill_options, 1):
            current_level = self.passive_skills.get(skill, 0)
            print(f"{i}. {skill} (当前等级: {current_level})")
        
        try:
            choice = int(input("输入编号选择技能: ")) - 1
            if 0 <= choice < len(skill_options):
                selected_skill = skill_options[choice]
                self.passive_skills[selected_skill] += 1
                print(f"获得新技能: {selected_skill} Lv{self.passive_skills[selected_skill]}")
            else:
                print("无效选择，随机分配技能")
                selected_skill = random.choice(skill_options)
                self.passive_skills[selected_skill] += 1
                print(f"获得新技能: {selected_skill} Lv{self.passive_skills[selected_skill]}")
        except ValueError:
            print("无效输入，随机分配技能")
            selected_skill = random.choice(skill_options)
            self.passive_skills[selected_skill] += 1
            print(f"获得新技能: {selected_skill} Lv{self.passive_skills[selected_skill]}")
    
    def consume_stamina(self, amount):
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        else:
            print(f"体力不足！当前体力: {self.stamina}/{self.max_stamina}")
            
            edible = [item for item in ['生肉', '熏肉', '鱼', '熏鱼'] if self.inventory[item] > 0]
            if edible:
                print("你可以食用以下食物补充体力:")
                for i, item in enumerate(edible, 1):
                    print(f"{i}. {item}")
                
                try:
                    choice = int(input("选择要食用的食物(输入编号，0取消): "))
                    if 1 <= choice <= len(edible):
                        food_type = edible[choice-1]
                        stamina_amount = {
                            '生肉': 20,
                            '熏肉': 30,
                            '鱼': 25,
                            '熏鱼': 40
                        }.get(food_type, 0)
                        heal_amount = {
                            '生肉': 15,
                            '熏肉': 25,
                            '鱼': 20,
                            '熏鱼': 30
                        }.get(food_type, 0)
                        energy_amount = {
                            '生肉': 5,
                            '熏肉': 8,
                            '鱼': 6,
                            '熏鱼': 10
                        }.get(food_type, 0)
                        
                        self.stamina = min(self.max_stamina, self.stamina + stamina_amount)
                        self.health = min(self.max_health, self.health + heal_amount)
                        self.energy = min(self.max_energy, self.energy + energy_amount)
                        self.inventory[food_type] -= 1
                        self.last_eaten = datetime.now()
                        
                        print(f"食用{food_type}，恢复了{stamina_amount}体力")
                        return self.stamina >= amount
                    else:
                        print("取消进食")
                except ValueError:
                    print("无效输入")
            
            return False
    
    def consume_energy(self, amount):
        if self.energy >= amount:
            self.energy -= amount
            return True
        else:
            print(f"精力不足！当前精力: {self.energy}/{self.max_energy}")
            return False
    
   
    
    def eat_food(self):
        print("\n可食用物品:")
        edible = []
        for item in ['生肉', '熏肉', '鱼', '熏鱼', '药膏']:
            if self.inventory[item] > 0:
                edible.append(item)
        
        if not edible:
            print("没有可食用的食物")
            return
        
        for i, item in enumerate(edible, 1):
            print(f"{i}. {item}")
        
        try:
            choice = int(input("选择要食用的食物(输入编号): ")) - 1
            if 0 <= choice < len(edible):
                food_type = edible[choice]
                heal_amount = {
                    '生肉': 15,
                    '熏肉': 25,
                    '鱼': 20,
                    '熏鱼': 30,
                    '药膏': 40 + self.level
                }.get(food_type, 0)
                
                stamina_amount = {
                    '生肉': 20,
                    '熏肉': 30,
                    '鱼': 25,
                    '熏鱼': 40,
                    '药膏': 0
                }.get(food_type, 0)
                
                energy_amount = {
                    '生肉': 5,
                    '熏肉': 8,
                    '鱼': 6,
                    '熏鱼': 10,
                    '药膏': 0
                }.get(food_type, 0)
                
                self.health = min(self.max_health, self.health + heal_amount)
                self.stamina = min(self.max_stamina, self.stamina + stamina_amount)
                self.energy = min(self.max_energy, self.energy + energy_amount)
                self.inventory[food_type] -= 1
                self.last_eaten = datetime.now()
                
                print(f"食用{food_type}，恢复了{heal_amount}生命、{stamina_amount}体力和{energy_amount}精力")
                
                if food_type in ['熏肉', '熏鱼']:
                    self.health_points = min(50, self.health_points + 1)
                elif food_type in ['生肉', '鱼']:
                    self.health_points = max(0, self.health_points - 1)
                
                
                
                if self.active_pets:
                    for pet in self.active_pets:
                        pet.feed()
                        print(f"{pet.name}也吃饱了！")
                
                self.gain_exp(5)
            else:
                print("无效选择！")
        except ValueError:
            print("请输入有效的数字")
    
    def sleep(self):
        print("\n============== 休息 ==============")
        if not self.check_pet_hunger():
            print("有宠物过于饥饿，你无法安心休息！")
       
        heal_amount = int(self.max_health * 0.2)
        self.health = min(self.max_health, self.health + heal_amount)
        self.stamina = self.max_stamina
        self.energy = self.max_energy
        
        if self.health >= self.max_health * 0.8:
            self.consecutive_healthy_days += 1
            if self.consecutive_healthy_days >= 3:
                self.health_points = min(50, self.health_points + 1)
                self.consecutive_healthy_days = 0
                print("连续保持健康，健康值+1")
        else:
            self.consecutive_healthy_days = 0
       
        if self.inventory['木头'] >= 2 and self.inventory['纤维'] >= 1:
            choice = input("要搭建帐篷吗？(消耗2木头和1纤维)(y/n): ").lower()
            if choice == 'y':
                self.inventory['木头'] -= 2
                self.inventory['纤维'] -= 1
                extra_heal = int(self.max_health * 0.2)
                self.health = min(self.max_health, self.health + extra_heal)
                print(f"你搭建了帐篷，额外恢复了{extra_heal}点生命值")
                self.health_points = min(50, self.health_points + 1)
            else:
                if random.random() < 0.6:
                    damage = int(self.max_health * 0.3)
                    self.health -= damage
                    print(f"你受凉了，损失了{damage}点生命值")
                    self.health_points = max(0, self.health_points - 1)
        else:
            print("没有足够的材料搭建帐篷...")
            if random.random() < 0.6:
                damage = int(self.max_health * 0.3)
                self.health -= damage
                print(f"你受凉了，损失了{damage}点生命值")
                self.health_points = max(0, self.health_points - 1)
        
        for pet in self.active_pets:
            pet.hunger += 1
            if pet.hunger >= 10:
                print(f"\n警告：{pet.name}非常饥饿！明天必须喂食！")
        
        self.day += 1
        print(f"\n第{self.day}天开始了！")
        print("体力和精力完全恢复")
        self.gain_exp(5)
    
    def upgrade_equipment(self):
        print("\n============== 装备升级 ==============")
        print(f"当前武器等级: {self.sword_level}")
        print(f"当前护甲等级: {self.armor_level}")
        
        options = []
        if self.inventory['水晶'] >= 3:
            options.append(('用水晶祈祷', '消耗3水晶提高最大生命'))
            
        if self.inventory['石头'] >= 5 and self.inventory['木头'] >= 3:
            options.append(('升级武器', '消耗5石头和3木头提升武器等级'))
        if self.inventory['兽皮'] >= 8 or self.inventory['纤维'] >= 8:
            options.append(('升级护甲', '消耗8兽皮或8纤维提升护甲等级'))
        
        if not options:
            print("没有足够的材料升级装备")
            return
        
        for i, (name, desc) in enumerate(options, 1):
            print(f"{i}. {name}: {desc}")
        
        try:
            choice = int(input("选择要升级的装备(输入编号): ")) - 1
            if 0 <= choice < len(options):
                action = options[choice][0]
                if action == '用水晶祈祷':
                    self.inventory['水晶'] -= 3
                    self.max_health += 15
                    self.health = min(self.max_health, self.health + 15)
                    print("使用水晶制作了护身符，最大生命值+15")
                if action == '升级武器':
                    self.inventory['石头'] -= 5
                    self.inventory['木头'] -= 3
                    self.sword_level += 1
                    print("武器等级提升1级！")
                elif action == '升级护甲':
                    if self.inventory['兽皮'] >=8:
                        self.inventory['兽皮'] -= 8
                    else:
                        self.inventory['纤维'] -= 8
                    self.armor_level += 1
                    print("护甲等级提升1级！")
                
                self.gain_exp(10)
            else:
                print("无效选择！")
        except ValueError:
            print("请输入有效的数字")
    
    def manage_pets(self):
        print("\n============== 宠物管理 ==============")
        if not self.pets:
            print("你还没有宠物")
            return
        
        print("你的宠物:")
        for i, pet in enumerate(self.pets, 1):
            hunger_status = "饥饿" if pet.hunger >= 8 else "正常"
            print(f"{i}. {pet.name} ({pet.type}, Lv{pet.level}, 状态: {hunger_status})")
        print("\n当前携带的宠物:")
        for i, pet in enumerate(self.active_pets, 1):
            print(f"{i}. {pet.name} ({pet.type})") 
        
        print("\n选项:")
        print("1. 携带宠物")
        print("2. 放回宠物")
        print("3. 喂食宠物")
        print("4. 返回")
        
        try:
            choice = int(input("选择操作(输入编号): "))
            
            if choice == 1:
                if len(self.active_pets) >= 3:
                    print("已经携带3只宠物了，请先放回一些")
                    return
                
                pet_idx = int(input("选择要携带的宠物(输入编号): ")) - 1
                if 0 <= pet_idx < len(self.pets):
                    if len(self.active_pets) < 3:
                        self.active_pets.append(self.pets[pet_idx])
                        print(f"现在携带{self.pets[pet_idx].name}")
                        self.check_evolution()
                    else:
                        print("已经携带3只宠物了")
                else:
                    print("无效选择！")
            
            elif choice == 2:
                if not self.active_pets:
                    print("当前没有携带宠物")
                    return
                
                print("当前携带的宠物:")
                for i, pet in enumerate(self.active_pets, 1):
                    print(f"{i}. {pet.name}")
                
                pet_idx = int(input("选择要放回的宠物(输入编号): ")) - 1
                if 0 <= pet_idx < len(self.active_pets):
                    print(f"已将{self.active_pets[pet_idx].name}放回")
                    self.active_pets.pop(pet_idx)
                else:
                    print("无效选择！")
            
            elif choice == 3:
                if not self.pets:
                    print("没有宠物可以喂食")
                    return
                
                pet_idx = int(input("选择要喂食的宠物(输入编号): ")) - 1
                if 0 <= pet_idx < len(self.pets):
                    if self.inventory['生肉'] > 0 or self.inventory['鱼'] > 0:
                        food_choice = input("选择喂食的食物(1.生肉 2.鱼): ")
                        if food_choice == '1' and self.inventory['生肉'] > 0:
                            self.inventory['生肉'] -= 1
                            self.pets[pet_idx].feed()
                            print(f"{self.pets[pet_idx].name}吃饱了！")
                        elif food_choice == '2' and self.inventory['鱼'] > 0:
                            self.inventory['鱼'] -= 1
                            self.pets[pet_idx].feed()
                            print(f"{self.pets[pet_idx].name}吃饱了！")
                        else:
                            print("没有足够的食物")
                    else:
                        print("没有可喂食的食物")
                else:
                    print("无效选择！")
            
            elif choice == 4:
                return
            
            else:
                print("无效选择！")
        except ValueError:
            print("请输入有效的数字")
    def check_evolution(self):
        if len(self.active_pets) >= 3: 
            type_counts = defaultdict(int)
            for pet in self.active_pets:
                type_counts[pet.type] += 1
      
            for pet_type, count in type_counts.items():
                if count >= 3:  
                    same_type_pets = [p for p in self.active_pets if p.type == pet_type]
                    same_type_pets.sort(key=lambda x: x.level, reverse=True)  
                    total_level = sum(p.level for p in same_type_pets[:3])
                    new_level = total_level // 2
                    
               
                    evolved_pet = copy.deepcopy(same_type_pets[0])  
                    evolved_pet.level = new_level
                    evolved_pet.evolution += 1 
                
                
                    new_name = input(f"要给进化后的{pet_type}起个新名字吗？(留空保持原名): ")
                    if new_name:
                        evolved_pet.name = new_name
                    
               
                    for pet in same_type_pets[:3]:
                        self.active_pets.remove(pet)
                    
              
                    self.active_pets.append(evolved_pet)
                
                    print(f"{pet_type}进化成功！新宠物: {evolved_pet.name}, 星级: {evolved_pet.evolution}, 等级: {evolved_pet.level}")
                    break  

def forest_event(player):
    print("\n============== 森林探索 ==============")
    
    if not player.consume_stamina(15) or not player.consume_energy(10):
        return
    
    
    wood_gain = random.randint(3, 5)
    fibre_gain = random.randint(1, 3)
    
   
    pet_bonus = 1.0
    if player.active_pets:
        total_pet_level = sum(p.level for p in player.active_pets)
        total_stars = sum(player.pet_evolution[p.name] for p in player.active_pets)
        
       
        pet_bonus += len(player.active_pets) * 0.03 + total_stars * 0.02 + total_pet_level * 0.01
        
        print(f"宠物团队帮你寻找资源！(加成:{int((pet_bonus-1)*100)}%)")
    
    if "采集效率+" in player.passive_skills:
        pet_bonus += player.passive_skills["采集效率+"] * 0.1
    
    wood_gain = int(wood_gain * pet_bonus)
    fibre_gain = int(fibre_gain * pet_bonus)
    
    player.inventory['木头'] += wood_gain
    player.inventory['纤维'] += fibre_gain
    print(f"收集到木头×{wood_gain}和纤维×{fibre_gain}")
    
    action = input("\n要采集浆果吗？(消耗5体力)(y/n): ").lower()
    if action == 'y' and player.consume_stamina(5):
        if random.random() < 0.7:
            heal = random.randint(10, 25)
            player.health = min(player.max_health, player.health + heal)
            stm = random.randint(10, 15)
            player.stamina = min(player.max_stamina, player.stamina + stm)
            eng = random.randint(2, 5)
            player.energy = min(player.max_energy, player.energy + eng)
            print(f"浆果很美味，恢复了{heal}点生命值,{stm}点体力,{eng}点精力！")
            player.health_points = min(50, player.health_points + 1)
        else:
            damage = random.randint(10, 20)
            player.health -= damage
            print(f"浆果有毒！你损失了{damage}点生命值！")
            player.health_points = max(0, player.health_points - 1)
    
   
    if random.random() < 0.3:
        beast_event(player, "森林")
    
   
    if random.random() < 0.2 and len(player.pets) < 15:
        pet_types = ["小狗", "小猫", "狐狸", "狼崽", "熊崽", "小猪"]
        new_pet = Pet(f"未命名", random.choice(pet_types))
        player.pets.append(new_pet)
        print(f"\n你在森林中发现了一只可爱的{new_pet.type}！")
        name = input("给你的新宠物起个名字: ")
        new_pet.name = name
        print(f"{name}加入了你的队伍！")

def cave_event(player):
    print("\n============== 洞穴探索 ==============")
    
    if not player.consume_stamina(20) or not player.consume_energy(10):
        return
    
    
    if random.random() > 0.7:  
        stone_gain = random.randint(3, 5) 
        
       
        pet_bonus = 1.0
        if player.active_pets:
            total_pet_level = sum(p.level for p in player.active_pets)
            total_stars = sum(player.pet_evolution[p.name] for p in player.active_pets)
        
       
            pet_bonus += len(player.active_pets) * 0.03 + total_stars * 0.02 + total_pet_level * 0.01
        
            print(f"宠物团队帮你寻找资源！(加成:{int((pet_bonus-1)*100)}%)")
        if "采集效率+" in player.passive_skills:
            pet_bonus += player.passive_skills["采集效率+"] * 0.1
        stone_gain = int(stone_gain * pet_bonus)
        
        player.inventory['石头'] += stone_gain
        print(f"发现石头×{stone_gain}")
    else:  
        beast_event(player, "洞穴")
    
    
    if player.inventory['钥匙'] > 0:
        action = input("\n要打开洞穴深处的宝箱吗？(消耗10体力)(y/n): ").lower()
        if action == 'y' and player.consume_stamina(10):
            if random.random() < 0.3:  
                player.inventory['钥匙'] -= 1
                print("钥匙损坏了！")
            else:
                print("钥匙还能继续使用")
            
            luck = random.random()
            if luck < 0.1:
                player.max_health += 20
                player.health = min(player.max_health, player.health + 20)
                print("找到生命药水！永久增加20点最大生命值")
            elif luck < 0.4:
                player.sword_level += 2
                print("找到强化石！武器等级+2")
            elif luck < 0.7:
                player.armor_level += 2
                print("找到护甲片！护甲等级+2")
            elif luck < 0.9:
                player.inventory['石头'] += 3
                player.inventory['木头'] += 3
                player.inventory['兽皮'] += 3
                print("找到资源包！获得一些基础资源")
            else:
                print("请选择一个技能")
                print("1.黑虎掏心 2.闪避 3.毒杀 4.熊躯 5.撕咬 6.吸血 7.冲撞 8.粘液")
                skill_options = ["黑虎掏心", "闪避", "毒杀", "熊躯", "撕咬", "吸血", "冲撞", "粘液"]
                try:
                    cave_skill_number = int(input("输入编号选择技能: ")) - 1
        
                    if 0 <= cave_skill_number < len(skill_options):
                        cave_skill = skill_options[cave_skill_number]
                        
                        player.monster_skills[cave_skill] += 1
                        print(f"获得了技能: {cave_skill}")
                    else:
                        print("无效选择，随机分配技能")
                        cave_skill = random.choice(skill_options)
                        
                        player.monster_skills[cave_skill] = +1
                        print(f"获得了技能: {cave_skill}")
                except ValueError:
                    print("无效输入，随机分配技能")
                    cave_skill = random.choice(skill_options)
                   
                    player.monster_skills[cave_skill] = +1
                    print(f"获得了技能: {cave_skill}")
            
            
            player.gain_exp(15)
    else:
        print("\n洞穴深处有个上锁的宝箱，但你没有钥匙")

def beach_event(player):
    print("\n============== 沙滩探索 ==============")
    
    if not player.consume_stamina(10) or not player.consume_energy(10):
        return
    
    
    if random.random() < 0.7:  
        player.inventory['钥匙'] += 1
        print("找到1把钥匙！")
    else:
        found = random.choice([
            ('木头', random.randint(3, 5)),
            ('纤维', random.randint(2, 4)),
            ('盐', random.randint(1, 2))
        ])
        player.inventory[found[0]] += found[1]
        print(f"找到{found[0]}×{found[1]}")
    
    
    action = input("\n要在海边捕鱼吗？(消耗10体力)(y/n): ").lower()
    if action == 'y' and player.consume_stamina(10):
        fish_chance = random.random()
        if fish_chance < 0.7:
            fish_amount = random.randint(1, 2)
            
           
            pet_bonus = 1.0
            if player.active_pets:
                total_pet_level = sum(p.level for p in player.active_pets)
                total_stars = sum(player.pet_evolution[p.name] for p in player.active_pets)
        
        
                pet_bonus += len(player.active_pets) * 0.03 + total_stars * 0.02 + total_pet_level * 0.01
        
                print(f"宠物团队帮你寻找资源！(加成:{int((pet_bonus-1)*100)}%)")
            fish_amount = int(fish_amount * pet_bonus)
            
            player.inventory['鱼'] += fish_amount 
            
            print(f"捕到了{fish_amount}条鱼!")
        else:
            print("今天没有捕到鱼")
    
    if random.random() < 0.5:
        salt_amount = random.randint(1, 2)
        player.inventory['盐'] += salt_amount
        print(f"在沙滩上收集到盐×{salt_amount}")
    
    
    player.gain_exp(10)

def lake_event(player):
    print("\n============== 湖泊探索 ==============")
    
    if not player.consume_stamina(10) or not player.consume_energy(10):
        return
    
    fish_chance = random.random()
    if fish_chance < 0.7:
        fish_amount = random.randint(2, 4)
        
        
        pet_bonus = 1.0
        if player.active_pets:
            total_pet_level = sum(p.level for p in player.active_pets)
            total_stars = sum(player.pet_evolution[p.name] for p in player.active_pets)
        
       
            pet_bonus += len(player.active_pets) * 0.03 + total_stars * 0.02 + total_pet_level * 0.01
        
            print(f"宠物团队帮你寻找资源！(加成:{int((pet_bonus-1)*100)}%)")
        fish_amount = int(fish_amount * pet_bonus)
            
        player.inventory['鱼'] += fish_amount 
        
        print(f"钓到了{fish_amount}条鱼！(保质期24小时)")
    else:
        print("今天鱼儿不上钩...")
    
   
    if random.random() < 0.4:
        herb_amount = random.randint(1, 2)
        player.inventory['草药'] += herb_amount
        print(f"在湖边发现了草药×{herb_amount}")
    
   
    player.gain_exp(10)

def mountain_event(player):
    print("\n============== 山脉探索 ==============")
    
    if not player.consume_stamina(20) or not player.consume_energy(10):
        return
    
   
    resource = random.choice([
        ('水晶', 2),
        ('草药', 3),
        ('石头', 4),
        ('盐', 2)
    ])
    
   
    pet_bonus = 1.0
    if player.active_pets:
        total_pet_level = sum(p.level for p in player.active_pets)
        total_stars = sum(player.pet_evolution[p.name] for p in player.active_pets)
        
        
        pet_bonus += len(player.active_pets) * 0.03 + total_stars * 0.02 + total_pet_level * 0.01
        
        print(f"宠物团队帮你寻找资源！(加成:{int((pet_bonus-1)*100)}%)")
           
    if "采集效率+" in player.passive_skills:
        pet_bonus += player.passive_skills["采集效率+"] * 0.1
    resource_gain = int(resource[1] * pet_bonus)
    
    player.inventory[resource[0]] += resource_gain
    print(f"发现{resource[0]}×{resource_gain}")
    
   
    
       
    
  
    if random.random() < 0.4:
        beast_event(player, "山脉")
    
   
    player.gain_exp(15)

def ruins_event(player):
    print("\n============== 遗迹探索 ==============")
    
    if not player.consume_stamina(30) or not player.consume_energy(10):
        return
    
    
    if not hasattr(player, 'ruins_level'):
        player.ruins_level = 1
    
    if not player.unlocked_secret:
        print("你发现了一处古老遗迹，似乎隐藏着岛屿的秘密...")
        player.unlocked_secret = True
        return
    
    print(f"\n当前遗迹层数: {player.ruins_level}")
    
    
    if random.random() < 0.1:
        print("你巧妙地避开了所有守卫，成功通过了这一层！")
        player.ruins_level += 1
        give_ruins_reward(player, player.ruins_level)
        return
    
   
    if random.random() < 0.9:
        if beast_event(player, "遗迹", is_ruins=True):
           
            player.ruins_level += 1
            give_ruins_reward(player, player.ruins_level)
        else:
            
            print("你被迫撤退，没能深入遗迹...")
    
    
    player.gain_exp(15)

def give_ruins_reward(player, level):
    """根据遗迹层数给予奖励"""
    print("\n=== 获得遗迹宝藏 ===")
    
    
    base_rewards = [
        ('水晶', level),
        ('草药', level * 2),
        ('钥匙', 1)
    ]
    
    for item, amount in base_rewards:
        player.inventory[item] += amount
        print(f"获得 {item}×{amount}")
    
   
    if level % 5 == 0:
        special_rewards = [
            ('永久生命药水', 1),  
            ('武器强化石', 1),   
            ('护甲强化片', 1),  
            ('神秘宠物蛋', 1)    
        ]
        reward = random.choice(special_rewards)
        
        if reward[0] == '永久生命药水':
            player.max_health += 50
            player.health = player.max_health
            print("使用永久生命药水，最大生命值+50！")
        elif reward[0] == '武器强化石':
            player.sword_level += 5
            print("使用武器强化石，武器等级+5！")
        elif reward[0] == '护甲强化片':
            player.armor_level += 5
            print("使用护甲强化片，护甲等级+5！")
        elif reward[0] == '神秘宠物蛋':
            pet_types = ["龙", "凤凰", "独角兽", "狮鹫"]
            new_pet = Pet(f"遗迹守护者{level}", random.choice(pet_types))
            new_pet.level = max(10, level // 2)
            player.pets.append(new_pet)
            print(f"孵化出{new_pet.name}！这是一只{new_pet.type}，初始等级{new_pet.level}")
    
   

def shipyard_event(player):
    print("\n============== 船坞 ==============")
    
    if not player.consume_stamina(10) or not player.consume_energy(10):
        return False
    
    if player.unlocked_ship:
        print(f"造船进度: 木头 {player.inventory['木头']}/100, 纤维 {player.inventory['纤维']}/50, 兽皮 {player.inventory['兽皮']}/20")
        if player.inventory['木头'] >= 100 and player.inventory['纤维'] >= 50 and player.inventory['兽皮'] >= 20:
            print("\n材料已齐备，可以立即启航！")
            print("恭喜你成功逃离了岛屿！")
            return True
        else:
            print("继续收集材料吧")
    else:
        print("你研究了破船的结构，学会了造船技术！")
        player.unlocked_ship = True
    
   
    player.gain_exp(10)
    return False

def beast_event(player, location):
    beast_types = {
        "森林": ["老虎", "狼", "野猪", "蜘蛛"],
        "洞穴": ["蝙蝠群", "蜘蛛", "蛇"],
        "山脉": ["熊", "鹰", "雪豹"],
        "湖泊": ["鳄鱼", "水蛇", "巨型青蛙"],
        "遗迹": ["守卫者""远古石像""亡灵祭司""变异巨兽"]
    }


    skill_options = {
        "老虎": "黑虎掏心",
        "狼": "闪避",
        "鹰": "闪避",
        "雪豹": "闪避",
        "蛇": "毒杀",
        "熊": "熊躯",
        "鳄鱼": "撕咬",
        "水蛇": "撕咬",
        "蜘蛛": "吸血",
        "蝙蝠群": "吸血",
        "野猪": "冲撞",
        "巨型青蛙": "粘液"
    }
    beast_type = random.choice(beast_types.get(location, ["野兽"]))
    beast_level = random.randint(max(1, player.level - 2), player.level + 2)
    if beast_type in ["守卫者""远古石像""亡灵祭司""变异巨兽"]:
        beast_level += 10
    print(f"\n你遇到了{beast_level}级{beast_type}，进入战斗！")
    
    
    beast_hp = beast_level * 30 + 150
    player_power = player.sword_level * 5
    beast_power = beast_level * 8
    
   
    if player.active_pets:
        total_pet_level = sum(p.level for p in player.active_pets)
        total_stars = sum(player.pet_evolution[p.name] for p in player.active_pets)
        
        player_power += len(player.active_pets) * 2 + total_stars * 1
         
        print(f"宠物团队协助你战斗！(攻击力+{len(player.active_pets)*2 + total_stars*1})")
    
    
    
   
    print("\n=========== 战斗开始 ===========")
    n = 2
    while player.health > 0 and beast_hp > 0:
        escape_choice = input("是否尝试逃跑？(y/n): ").lower()
        if escape_choice == 'y':
            escape_chance = 0.6  
            if "闪避" in player.monster_skills:
                escape_chance += player.monster_skills["闪避"] * 0.05  
            
            if random.random() < escape_chance:
                print("你成功逃脱了战斗！")
                player.health_points = max(0, player.health_points - 1)
                return False
            else:
                print("逃跑失败！怪物趁机攻击了你！")
                
                hurt = beast_power
                player.health -= hurt
                print(f"受到{hurt}点伤害")
                continue
        crit_chance = player.passive_skills.get("暴击率+", 0) * 0.05
        damage = player_power
        if random.random() < crit_chance:
            damage *= 2
            print("触发暴击！")
        
        beast_hp -= damage
        print(f"对{beast_type}造成{damage}点伤害")
        
   
        for skill, level in player.monster_skills.items():
            if skill == "黑虎掏心" :
                beast_hp -= (beast_level * 20 + 150 - beast_hp) * 4 // (beast_level * 20 + 150) * level
                print(f"使用技能黑虎掏心，对怪物造成{(beast_level*20+150-beast_hp)*4//(beast_level*20+150)*level}点附加伤害")
                player_power += level * 5
            elif skill == "毒杀" :
                beast_hp -= n * level
                print(f"使用技能毒杀，对怪物造成{n*level}点附加伤害")
            elif skill == "撕咬" :
                beast_hp -= 2 * level
                print(f"使用技能撕咬，对怪物造成{2 * level}点附加伤害")
            elif skill == "吸血":
                player.health = min(player.max_health, player.health + player.sword_level * level * 0.5)
                print(f"使用技能吸血技能恢复了{player.sword_level*level*0.5}点生命值")
            elif skill == "冲撞" :
                beast_power -= level * 1
                print(f"使用技能冲撞使怪物眩晕，降低其{level}点攻击力")
        if beast_hp > 0:
            hurt = beast_power
            for skill, level in player.monster_skills.items():
                if skill == "闪避":
                    if random.random() < level * 0.04 and random.random() < 0.8:
                        hurt = 0
                        print("触发技能闪避，免疫本次伤害")
                elif skill == "熊躯":
                    hurt = max(0, hurt - level * 2)
                    print(f"触发技能熊躯，抵挡{level*2}点伤害")
                elif skill == "粘液":
                    beast_hp -= int(hurt * level * 0.05)
                    print(f"触发技能粘液，对怪物造成{int(hurt*level*0.05)}点伤害")
            hurt = max(0,hurt-player.armor_level)
            player.health -= hurt
            print(f"受到{hurt}点伤害")
        if beast_hp <= 0 and player.health > 0:
            exp_gain = beast_level * 10
            if "战斗经验+" in player.passive_skills:
                exp_gain = int(exp_gain * (1 + player.passive_skills["战斗经验+"] * 0.1))
            if "生命恢复+" in player.passive_skills:
                player.health += player.passive_skills["生命恢复+"] * 5
        
            player.gain_exp(exp_gain)
            if player.active_pets:  
                pet_exp = beast_level * 5
                for pet in player.active_pets:
                    pet.gain_exp(pet_exp)
                    print(f"{pet.name}获得了{pet_exp}经验")
        
            print(f"\n战斗胜利！获得{exp_gain}经验值")
        
            loot_options = {
                "老虎": [('兽皮', 3), ('生肉', 2)],
                "狼": [('兽皮', 4), ('生肉', 1)],
                "野猪": [('兽皮', 3), ('生肉', 2)],
                "蜘蛛": [('纤维', 3), ('草药', 2)],
                "蝙蝠群": [('纤维', 5)],
                "蛇": [('兽皮', 2), ('草药', 3)],
                "熊": [('兽皮', 3), ('生肉', 2)],
                "鹰": [('纤维', 2), ('生肉', 3)],
                "雪豹": [('兽皮', 4), ('生肉', 1)],
                "鳄鱼": [('兽皮', 3), ('生肉', 2)],
                "水蛇": [('兽皮', 3), ('草药', 2)],
                "巨型青蛙": [('纤维', 4), ('生肉', 1)],
                "守卫者": [('水晶', 3), ('钥匙', 1)],
                "远古石像": [('石头', 5), ('水晶', 2)],
                "亡灵祭司": [('草药', 3), ('水晶', 2)],
                "变异巨兽": [('兽皮', 5), ('生肉', 5)]
            }    
        
            loot = random.choice(loot_options.get(beast_type, [('石头', 1), ('兽皮', 1)]))
            player.inventory[loot[0]] += loot[1]
        
        
            print(f"获得战利品: {loot[0]}×{loot[1]}")
           
            if random.random() < 0.3:
                extra_loot = ('兽皮', 5)
                player.inventory[extra_loot[0]] += extra_loot[1]
                print(f"额外获得: {extra_loot[0]}×{extra_loot[1]}")
       
            if beast_type in skill_options:
                skill = skill_options[beast_type]
       
                base_chance = 0.2
        
                if skill in player.monster_skills:
                    base_chance += 0.2
        
                if random.random() < base_chance:
                    player.monster_skills[skill] += 1
                    if player.monster_skills[skill] == 1:
                        print(f"领悟了{skill}技能！")
                    else:
                        print(f"{skill}技能升级到{player.monster_skills[skill]}级！")
            
   
   

            return True
        elif player.health <= 0:
            print("战斗失败")
            player.health_points -= 20
            player.health == 1
            return False
            
        else:
            print(f"剩余{player.health}血，怪物剩余{beast_hp}血")
            print(f"第{n}回合")
            n += 1
            


def process_food(player):
    print("\n============== 食物处理 ==============")
    options = []
    
    if player.inventory['草药'] >= 5:
        options.append(('制作药膏', '消耗5草药'))

    if player.inventory['生肉'] > 0 and player.inventory['木头'] > 0 and player.inventory['盐'] > 0:
        options.append(('熏制生肉', '消耗1木头将1生肉变成熏肉'))
    
    if player.inventory['鱼'] > 0 and player.inventory['木头'] > 0 and player.inventory['盐'] > 0:
        options.append(('熏制鱼', '消耗1木头和1盐将1鱼变成熏鱼'))
    
    if not options:
        print("没有可处理的食物或材料")
        return
    
    for i, (name, desc) in enumerate(options, 1):
        print(f"{i}. {name}: {desc}")
    
    try:
        choice = int(input("选择要进行的处理(输入编号): ")) - 1
        if 0 <= choice < len(options):
            action = options[choice][0]
            
            if action == '熏制生肉':
                if player.inventory['生肉'] < 1 or player.inventory['木头'] < 1 or player.inventory['盐'] < 1:
                    print("材料不足！")
                    return
                
                player.inventory['生肉'] -= 1
                player.inventory['木头'] -= 1
                player.inventory['盐'] -= 1
                player.inventory['熏肉'] += 1
                if '生肉' in player.food_expiry:
                    del player.food_expiry['生肉']
                print("成功熏制1块生肉")
                player.health_points = min(50, player.health_points + 1)
            
            elif action == '熏制鱼':
                if player.inventory['鱼'] < 1 or player.inventory['木头'] < 1 or player.inventory['盐'] < 1:
                    print("材料不足！")
                    return
                
                player.inventory['鱼'] -= 1
                player.inventory['木头'] -= 1
                player.inventory['盐'] -= 1
                player.inventory['熏鱼'] += 1
                if '鱼' in player.food_expiry:
                    del player.food_expiry['鱼']
                print("成功熏制1条鱼")
                player.health_points = min(50, player.health_points + 1)
            
            elif action == '制作药膏':
                if player.inventory['草药'] < 5:
                    print("材料不足！")
                    return
                
                player.inventory['草药'] -= 5
                player.inventory['药膏'] += 1
                print("获得一块药膏！")
            
           
            player.gain_exp(10)
        else:
            print("无效选择")
    except ValueError:
        print("请输入有效的数字")

def text_adventure():
    print("神秘岛冒险")
    print("请选择你的性别")
    gender = input("(f/m): ").lower()
    if gender == 'f':
        print("你选择了女性，好好生存下去吧")
    else:
        print("你选择了男性，好好生存下去吧")
    
    print("======================")
    print("你醒来发现自己在一个陌生的岛屿上...")
    print("请选择一个初始技能")
    print("1.黑虎掏心 2.闪避 3.毒杀 4.熊躯 5.撕咬 6.吸血 7.冲撞 8.粘液")
    skill_options = ["黑虎掏心", "闪避", "毒杀", "熊躯", "撕咬", "吸血", "冲撞", "粘液"]
    try:
        origin_skill_number = int(input("输入编号选择技能: ")) - 1
        
        if 0 <= origin_skill_number < len(skill_options):
            origin_skill = skill_options[origin_skill_number]
            player = Player()
            player.monster_skills[origin_skill] = 1
            print(f"获得了技能: {origin_skill}")
        else:
            print("无效选择，随机分配技能")
            origin_skill = random.choice(skill_options)
            player = Player()
            player.monster_skills[origin_skill] = 1
            print(f"获得了技能: {origin_skill}")
    except ValueError:
        print("无效输入，随机分配技能")
        origin_skill = random.choice(skill_options)
        player = Player()
        player.monster_skills[origin_skill] = 1
        print(f"获得了技能: {origin_skill}")
    
                    
    
    game_over = False
    locations = ['森林', '洞穴', '沙滩', '山脉', '湖泊']
    
    while not game_over:
       
        
        low_energy = player.energy <= 20
        low_stamina = player.stamina <= 20
        
        player.show_status()
       
        if player.health_points <= 0:
            print("\n你的健康状况恶化，无法继续冒险！")
            print("游戏结束！看广告复活牢大")
            reborn = input("是否观看30s广告复活？(y/n): ").lower()
            if reborn == 'y':
                print("牢大复活了，但是你死了")
            break
        
       
        for pet in player.active_pets:
            if pet.hunger >= 10:
                print(f"\n警告：{pet.name}饿坏了，拒绝协助你！")
          
        print("\n主菜单:")
        print("1. 探索地点")
        print("2. 食用食物")
        print("3. 处理食物/材料")
        print("4. 装备升级")
        print("5. 宠物管理")
        if low_energy or low_stamina:
            print("6. 休息(推荐)")
        else:
            print("6. 休息")
        print("7. 荒野之神的馈赠")
        
        try:
            menu_choice = int(input("选择要进行的操作(输入编号): "))
            
            if menu_choice == 1:
                if player.energy <= 0:
                    print("\n你太累了，需要休息！")
                    continue
                
                available_locations = random.sample(locations, 2)
                if player.unlocked_secret:
                    available_locations.append('遗迹')
                if player.unlocked_ship:
                    available_locations.append('船坞')
                
                print("\n你可以去:")
                for i, location in enumerate(available_locations, 1):
                    print(f"{i}. {location}")
                
                try:
                    choice = int(input("请选择要去的地方(输入编号): ")) - 1
                    
                    if 0 <= choice < len(available_locations):
                        current_location = available_locations[choice]
                        
                        if current_location == "森林":
                            forest_event(player)
                        elif current_location == "洞穴":
                            cave_event(player)
                        elif current_location == "沙滩":
                            beach_event(player)
                        elif current_location == "山脉":
                            mountain_event(player)
                        elif current_location == "湖泊":
                            lake_event(player)
                        elif current_location == "遗迹":
                            ruins_event(player)
                        elif current_location == "船坞":
                            if shipyard_event(player):
                                game_over = True
                                continue
                        if player.health <= 0:
                            player.health_points -= 20
                            player.health = 1

                        if player.health_points <= 0:
                            print("\n你死了...游戏结束！")
                            reborn = input("是否观看30s广告复活？(y/n): ").lower()
                            if reborn == 'y':
                                print("牢大复活了，但是你死了")
                            game_over = True
                    else:
                        print("无效选择！")
                
                except ValueError:
                    print("请输入有效的数字")
            
            elif menu_choice == 2:
                player.eat_food()
            
            elif menu_choice == 3:
                process_food(player)
            
            elif menu_choice == 4:
                player.upgrade_equipment()
            
            elif menu_choice == 5:
                player.manage_pets()
            
            elif menu_choice == 6:
                player.sleep()
            
            
            
            elif menu_choice == 7:
                print("\n============== 荒野之神的馈赠 ==============")
                print("你选择接受荒野之神的馈赠，请向神许愿")
                print("1. 获得所有物品各十份")
                print("2. 所有技能升一级")
                print("3. 获得2000经验")
                print("4. 推进游戏进度(解锁遗迹和船坞)")
                print("5. 随机获得一只宠物")
                print("6. 返回")
                
                try:
                    gift_type = int(input("输入编号选择馈赠种类: "))
                    
                    if gift_type == 1:
                        # 获得所有物品各十份
                        for item in player.inventory:
                            player.inventory[item] += 10
                        print("获得所有物品各十份！")
                        
                    elif gift_type == 2:
                        # 获得/升级技能
                        skill_options = [
                            "生命恢复+", "暴击率+", 
                            "采集效率+", "战斗经验+"
                        ]
                        monster_skill_options = [
                            "黑虎掏心", "闪避", "毒杀", "熊躯", 
                            "撕咬", "吸血", "冲撞", "粘液"
                        ]
                        
                        # 检查是否有被动技能
                        if not player.passive_skills:
                            # 如果没有被动技能，随机获得一个
                            selected_skill = random.choice(skill_options)
                            player.passive_skills[selected_skill] = 1
                            print(f"获得新被动技能: {selected_skill} Lv1")
                        else:
                            # 有被动技能则升级一个随机技能
                            skill = random.choice(list(player.passive_skills.keys()))
                            player.passive_skills[skill] += 1
                            print(f"{skill} 升级到 Lv{player.passive_skills[skill]}")
                        
                        # 检查是否有怪物技能
                        if not player.monster_skills:
                            # 如果没有怪物技能，随机获得一个
                            selected_skill = random.choice(monster_skill_options)
                            player.monster_skills[selected_skill] = 1
                            print(f"获得新怪物技能: {selected_skill} Lv1")
                        else:
                            # 有怪物技能则升级一个随机技能
                            skill = random.choice(list(player.monster_skills.keys()))
                            player.monster_skills[skill] += 1
                            print(f"{skill} 升级到 Lv{player.monster_skills[skill]}")
                               
                            
                    elif gift_type == 3:
                        # 获得2000经验
                        player.gain_exp(2000)
                        print("获得2000经验值！")
                        
                    elif gift_type == 4:
                        # 推进游戏进度
                        if not player.unlocked_secret:
                            player.unlocked_secret = True
                            print("解锁了遗迹探索！")
                        if not player.unlocked_ship:
                            player.unlocked_ship = True
                            print("解锁了船坞！")
                        print("游戏进度已推进！")
                        
                    elif gift_type == 5:
                        # 随机获得一只宠物
                        pet_types = ["小狗", "小猫", "狐狸", "狼崽", "熊崽", "小猪", "龙", "凤凰", "独角兽", "狮鹫"]
                        pet_type = random.choice(pet_types)
                        new_pet = Pet(f"神赐{pet_type}", pet_type)
                        
                        # 神赐宠物有较高初始等级
                        new_pet.level = random.randint(5, 15)
                        
                        player.pets.append(new_pet)
                        print(f"获得了一只{new_pet.level}级的{new_pet.type}，名为{new_pet.name}！")
                        
                    elif gift_type == 6:
                        continue
                        
                    else:
                        print("无效选择！")
                        
                except ValueError:
                    print("请输入有效的数字")
            
            else:
                print("无效选择！")
        
        except ValueError:
            print("请输入有效的数字")

if __name__ == "__main__":
    text_adventure()
                        
                        
            
   
