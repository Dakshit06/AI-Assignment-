"""
Interactive Expert System Using Forward Chaining
A computer troubleshooting expert system that uses forward chaining inference
"""

class Fact:
    """Represents a fact in the knowledge base"""
    def __init__(self, name, value=True):
        self.name = name
        self.value = value
    
    def __str__(self):
        return f"{self.name}: {self.value}"
    
    def __eq__(self, other):
        return isinstance(other, Fact) and self.name == other.name and self.value == other.value
    
    def __hash__(self):
        return hash((self.name, self.value))

class Rule:
    """Represents a rule in the knowledge base"""
    def __init__(self, conditions, conclusion, description=""):
        self.conditions = conditions  # List of Facts (antecedents)
        self.conclusion = conclusion  # Single Fact (consequent)
        self.description = description
        self.used = False
    
    def __str__(self):
        conditions_str = " AND ".join([str(cond) for cond in self.conditions])
        return f"IF {conditions_str} THEN {self.conclusion}"

class ForwardChainingEngine:
    """Forward chaining inference engine"""
    
    def __init__(self):
        self.facts = set()  # Known facts
        self.rules = []     # Rules in knowledge base
        self.fired_rules = []  # Rules that have been fired
        self.trace = []     # Inference trace
    
    def add_fact(self, fact):
        """Add a fact to the knowledge base"""
        if isinstance(fact, str):
            fact = Fact(fact)
        self.facts.add(fact)
        self.trace.append(f"Added fact: {fact}")
    
    def add_rule(self, rule):
        """Add a rule to the knowledge base"""
        self.rules.append(rule)
    
    def has_fact(self, fact):
        """Check if a fact exists in the knowledge base"""
        if isinstance(fact, str):
            fact = Fact(fact)
        return fact in self.facts
    
    def can_fire_rule(self, rule):
        """Check if a rule can be fired (all conditions are met)"""
        if rule.used:
            return False
        
        for condition in rule.conditions:
            if not self.has_fact(condition):
                return False
        return True
    
    def fire_rule(self, rule):
        """Fire a rule and add its conclusion as a new fact"""
        if self.can_fire_rule(rule):
            self.add_fact(rule.conclusion)
            rule.used = True
            self.fired_rules.append(rule)
            self.trace.append(f"Fired rule: {rule.description or str(rule)}")
            return True
        return False
    
    def forward_chain(self):
        """Perform forward chaining inference"""
        changed = True
        iteration = 0
        
        while changed:
            changed = False
            iteration += 1
            self.trace.append(f"\n--- Iteration {iteration} ---")
            
            for rule in self.rules:
                if self.fire_rule(rule):
                    changed = True
            
            if not changed:
                self.trace.append("No more rules can be fired.")
    
    def get_conclusions(self):
        """Get all derived conclusions"""
        return [fact for fact in self.facts]
    
    def print_trace(self):
        """Print the inference trace"""
        print("\n=== INFERENCE TRACE ===")
        for step in self.trace:
            print(step)

class ComputerTroubleshootingSystem:
    """Computer troubleshooting expert system using forward chaining"""
    
    def __init__(self):
        self.engine = ForwardChainingEngine()
        self.initialize_knowledge_base()
    
    def initialize_knowledge_base(self):
        """Initialize the computer troubleshooting knowledge base with rules"""
        
        # Define computer troubleshooting rules
        rules = [
            # Power Issues
            Rule(
                [Fact("computer_not_starting"), Fact("no_power_lights")],
                Fact("power_supply_issue"),
                "Power supply problem: computer not starting + no power lights"
            ),
            
            Rule(
                [Fact("computer_not_starting"), Fact("power_lights_on")],
                Fact("hardware_failure"),
                "Hardware failure: computer not starting but power lights on"
            ),
            
            # Boot Issues
            Rule(
                [Fact("computer_starts"), Fact("no_display")],
                Fact("display_issue"),
                "Display problem: computer starts but no display"
            ),
            
            Rule(
                [Fact("computer_starts"), Fact("blue_screen")],
                Fact("system_crash"),
                "System crash: computer starts but shows blue screen"
            ),
            
            Rule(
                [Fact("computer_starts"), Fact("slow_boot")],
                Fact("startup_optimization_needed"),
                "Startup optimization needed: computer starts but boots slowly"
            ),
            
            # Performance Issues
            Rule(
                [Fact("computer_running"), Fact("very_slow_performance")],
                Fact("performance_issue"),
                "Performance problem: computer running but very slow"
            ),
            
            Rule(
                [Fact("performance_issue"), Fact("high_cpu_usage")],
                Fact("cpu_overload"),
                "CPU overload: performance issue + high CPU usage"
            ),
            
            Rule(
                [Fact("performance_issue"), Fact("low_memory")],
                Fact("memory_shortage"),
                "Memory shortage: performance issue + low memory"
            ),
            
            # Network Issues
            Rule(
                [Fact("no_internet"), Fact("wifi_connected")],
                Fact("dns_issue"),
                "DNS problem: no internet but WiFi connected"
            ),
            
            Rule(
                [Fact("no_internet"), Fact("wifi_not_connected")],
                Fact("wifi_connection_issue"),
                "WiFi connection problem: no internet + WiFi not connected"
            ),
            
            # Storage Issues
            Rule(
                [Fact("computer_running"), Fact("disk_full_warning")],
                Fact("storage_full"),
                "Storage full: computer running but disk full warning"
            ),
            
            Rule(
                [Fact("file_corruption"), Fact("frequent_crashes")],
                Fact("hard_drive_failure"),
                "Hard drive failure: file corruption + frequent crashes"
            ),
            
            # Audio/Video Issues
            Rule(
                [Fact("no_sound"), Fact("speakers_connected")],
                Fact("audio_driver_issue"),
                "Audio driver problem: no sound but speakers connected"
            ),
            
            Rule(
                [Fact("display_issue"), Fact("monitor_connected")],
                Fact("graphics_driver_issue"),
                "Graphics driver problem: display issue but monitor connected"
            ),
            
            # Solution Rules
            Rule(
                [Fact("power_supply_issue")],
                Fact("check_power_connections"),
                "Solution: Check all power connections and cables"
            ),
            
            Rule(
                [Fact("hardware_failure")],
                Fact("run_hardware_diagnostics"),
                "Solution: Run hardware diagnostics and check RAM"
            ),
            
            Rule(
                [Fact("display_issue")],
                Fact("check_display_connections"),
                "Solution: Check monitor connections and try different cable"
            ),
            
            Rule(
                [Fact("system_crash")],
                Fact("check_recent_software_changes"),
                "Solution: Check recent software changes and boot in safe mode"
            ),
            
            Rule(
                [Fact("cpu_overload")],
                Fact("close_unnecessary_programs"),
                "Solution: Close unnecessary programs and check for malware"
            ),
            
            Rule(
                [Fact("memory_shortage")],
                Fact("add_more_ram"),
                "Solution: Close programs or add more RAM"
            ),
            
            Rule(
                [Fact("dns_issue")],
                Fact("reset_dns_settings"),
                "Solution: Reset DNS settings or use public DNS"
            ),
            
            Rule(
                [Fact("wifi_connection_issue")],
                Fact("restart_router_and_network_adapter"),
                "Solution: Restart router and network adapter"
            ),
            
            Rule(
                [Fact("storage_full")],
                Fact("clean_disk_space"),
                "Solution: Clean disk space and remove unnecessary files"
            ),
            
            Rule(
                [Fact("hard_drive_failure")],
                Fact("backup_data_immediately"),
                "Solution: Backup data immediately and replace hard drive"
            ),
            
            Rule(
                [Fact("audio_driver_issue")],
                Fact("update_audio_drivers"),
                "Solution: Update or reinstall audio drivers"
            ),
            
            Rule(
                [Fact("graphics_driver_issue")],
                Fact("update_graphics_drivers"),
                "Solution: Update or reinstall graphics drivers"
            ),
            
            Rule(
                [Fact("startup_optimization_needed")],
                Fact("disable_startup_programs"),
                "Solution: Disable unnecessary startup programs"
            ),
            
            # Priority/Urgency Rules
            Rule(
                [Fact("hard_drive_failure")],
                Fact("urgent_attention_required"),
                "URGENT: Hard drive failure requires immediate attention"
            ),
            
            Rule(
                [Fact("power_supply_issue")],
                Fact("high_priority_issue"),
                "HIGH PRIORITY: Power supply issues can damage components"
            ),
            
            Rule(
                [Fact("system_crash")],
                Fact("medium_priority_issue"),
                "MEDIUM PRIORITY: System crashes need prompt attention"
            )
        ]
        
        # Add all rules to the engine
        for rule in rules:
            self.engine.add_rule(rule)
    
    def ask_computer_issues(self):
        """Interactive computer issue assessment"""
        print("\n=== COMPUTER TROUBLESHOOTING EXPERT SYSTEM ===")
        print("Please answer the following questions with 'yes' or 'no':")
        print("This will help diagnose your computer issues.\n")
        
        # Power and Boot Issues
        print("=== POWER & BOOT ISSUES ===")
        power_boot_issues = [
            "computer_not_starting", "no_power_lights", "power_lights_on",
            "computer_starts", "no_display", "blue_screen", "slow_boot"
        ]
        
        for issue in power_boot_issues:
            while True:
                question = self.format_question(issue)
                response = input(f"{question} (yes/no): ").lower().strip()
                if response in ['yes', 'y']:
                    self.engine.add_fact(Fact(issue))
                    break
                elif response in ['no', 'n']:
                    break
                else:
                    print("Please answer 'yes' or 'no'")
        
        # Performance Issues
        print("\n=== PERFORMANCE ISSUES ===")
        performance_issues = [
            "computer_running", "very_slow_performance", "high_cpu_usage",
            "low_memory", "frequent_crashes"
        ]
        
        for issue in performance_issues:
            while True:
                question = self.format_question(issue)
                response = input(f"{question} (yes/no): ").lower().strip()
                if response in ['yes', 'y']:
                    self.engine.add_fact(Fact(issue))
                    break
                elif response in ['no', 'n']:
                    break
                else:
                    print("Please answer 'yes' or 'no'")
        
        # Network Issues
        print("\n=== NETWORK ISSUES ===")
        network_issues = [
            "no_internet", "wifi_connected", "wifi_not_connected"
        ]
        
        for issue in network_issues:
            while True:
                question = self.format_question(issue)
                response = input(f"{question} (yes/no): ").lower().strip()
                if response in ['yes', 'y']:
                    self.engine.add_fact(Fact(issue))
                    break
                elif response in ['no', 'n']:
                    break
                else:
                    print("Please answer 'yes' or 'no'")
        
        # Storage and Hardware Issues
        print("\n=== STORAGE & HARDWARE ISSUES ===")
        storage_hardware_issues = [
            "disk_full_warning", "file_corruption", "no_sound",
            "speakers_connected", "monitor_connected"
        ]
        
        for issue in storage_hardware_issues:
            while True:
                question = self.format_question(issue)
                response = input(f"{question} (yes/no): ").lower().strip()
                if response in ['yes', 'y']:
                    self.engine.add_fact(Fact(issue))
                    break
                elif response in ['no', 'n']:
                    break
                else:
                    print("Please answer 'yes' or 'no'")
    
    def format_question(self, issue):
        """Format issue name into a readable question"""
        question_map = {
            "computer_not_starting": "Is your computer not starting at all?",
            "no_power_lights": "Are there no power lights/LEDs visible?",
            "power_lights_on": "Are the power lights/LEDs on?",
            "computer_starts": "Does your computer start/power on?",
            "no_display": "Is there no display on your monitor?",
            "blue_screen": "Do you see a blue screen error?",
            "slow_boot": "Does your computer boot very slowly?",
            "computer_running": "Is your computer currently running?",
            "very_slow_performance": "Is your computer running very slowly?",
            "high_cpu_usage": "Is your CPU usage consistently high?",
            "low_memory": "Are you getting low memory warnings?",
            "frequent_crashes": "Does your computer crash frequently?",
            "no_internet": "Do you have no internet connection?",
            "wifi_connected": "Is WiFi showing as connected?",
            "wifi_not_connected": "Is WiFi not connecting?",
            "disk_full_warning": "Are you getting disk full warnings?",
            "file_corruption": "Are you experiencing file corruption?",
            "no_sound": "Is there no sound from your computer?",
            "speakers_connected": "Are speakers/headphones connected?",
            "monitor_connected": "Is your monitor properly connected?"
        }
        return question_map.get(issue, f"Do you have {issue.replace('_', ' ')}?")
    
    def diagnose(self):
        """Perform diagnosis using forward chaining"""
        print("\n=== ANALYZING COMPUTER ISSUES ===")
        self.engine.forward_chain()
        
        # Extract problems and solutions
        problems = []
        solutions = []
        priorities = []
        
        for fact in self.engine.facts:
            fact_name = fact.name
            
            # Identify problems
            if fact_name in ["power_supply_issue", "hardware_failure", "display_issue", 
                           "system_crash", "cpu_overload", "memory_shortage", "dns_issue",
                           "wifi_connection_issue", "storage_full", "hard_drive_failure",
                           "audio_driver_issue", "graphics_driver_issue", "startup_optimization_needed",
                           "performance_issue"]:
                problems.append(fact_name.replace("_", " ").title())
            
            # Identify solutions
            elif fact_name.startswith("check_") or fact_name.startswith("run_") or \
                 fact_name.startswith("close_") or fact_name.startswith("add_") or \
                 fact_name.startswith("reset_") or fact_name.startswith("restart_") or \
                 fact_name.startswith("clean_") or fact_name.startswith("backup_") or \
                 fact_name.startswith("update_") or fact_name.startswith("disable_"):
                solutions.append(fact_name.replace("_", " ").title())
            
            # Identify priorities
            elif "priority" in fact_name or "urgent" in fact_name:
                priorities.append(fact_name.replace("_", " ").title())
        
        return problems, solutions, priorities
    
    def print_results(self, problems, solutions, priorities):
        """Print troubleshooting results"""
        print("\n" + "="*60)
        print("COMPUTER TROUBLESHOOTING RESULTS")
        print("="*60)
        
        if priorities:
            print("\n🚨 PRIORITY ALERTS:")
            for priority in priorities:
                print(f"   • {priority}")
        
        if problems:
            print("\n🔍 IDENTIFIED PROBLEMS:")
            for problem in problems:
                print(f"   • {problem}")
        else:
            print("\n🔍 No specific problems identified from the given symptoms.")
            print("   Your computer issues might require further investigation.")
        
        if solutions:
            print("\n🔧 RECOMMENDED SOLUTIONS:")
            for i, solution in enumerate(solutions, 1):
                print(f"   {i}. {solution}")
        
        print("\n📋 ALL IDENTIFIED FACTS:")
        for fact in sorted(self.engine.facts, key=lambda x: x.name):
            if not fact.name.startswith("computer_") and not fact.name.startswith("no_") and \
               not fact.name.startswith("wifi_") and not fact.name.startswith("power_") and \
               not fact.name.startswith("high_") and not fact.name.startswith("low_") and \
               not fact.name.startswith("very_") and not fact.name.startswith("slow_") and \
               not fact.name.startswith("disk_") and not fact.name.startswith("file_") and \
               not fact.name.startswith("speakers_") and not fact.name.startswith("monitor_") and \
               not fact.name.startswith("frequent_") and not fact.name.startswith("blue_"):
                print(f"   • {fact.name.replace('_', ' ').title()}")
        
        print("\n💡 GENERAL TIPS:")
        print("   • Restart your computer if you haven't already")
        print("   • Check for Windows updates")
        print("   • Run a virus scan")
        print("   • Create a backup of important data")
    
    def run_demo(self):
        """Run a demo with predefined computer issues"""
        print("\n=== DEMO MODE ===")
        print("Running demo with predefined computer issues...")
        
        # Demo case 1: Performance issues
        demo_issues = ["computer_running", "very_slow_performance", "high_cpu_usage"]
        print(f"Demo issues: {', '.join([issue.replace('_', ' ') for issue in demo_issues])}")
        
        for issue in demo_issues:
            self.engine.add_fact(Fact(issue))
        
        problems, solutions, priorities = self.diagnose()
        self.print_results(problems, solutions, priorities)
        
        if input("\nShow inference trace? (y/n): ").lower() == 'y':
            self.engine.print_trace()
    
    def run_interactive(self):
        """Run interactive computer troubleshooting"""
        self.ask_computer_issues()
        problems, solutions, priorities = self.diagnose()
        self.print_results(problems, solutions, priorities)
        
        if input("\nShow inference trace? (y/n): ").lower() == 'y':
            self.engine.print_trace()

def main():
    """Main function"""
    print("Forward Chaining Expert System - Computer Troubleshooting")
    print("="*65)
    
    while True:
        print("\nChoose an option:")
        print("1. Interactive Computer Troubleshooting")
        print("2. Demo Mode")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            system = ComputerTroubleshootingSystem()
            system.run_interactive()
        elif choice == '2':
            system = ComputerTroubleshootingSystem()
            system.run_demo()
        elif choice == '3':
            print("Thank you for using the Computer Troubleshooting Expert System!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()