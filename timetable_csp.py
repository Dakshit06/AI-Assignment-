import random
from typing import Dict, List, Tuple, Set

class TimetableCSP:
    def __init__(self):
        # Define the domains
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.time_slots = ['9:00-10:00', '10:00-11:00', '11:00-12:00', '14:00-15:00', '15:00-16:00']
        self.subjects = ['Math', 'Physics', 'Chemistry', 'English', 'History']
        self.teachers = ['Teacher_A', 'Teacher_B', 'Teacher_C', 'Teacher_D', 'Teacher_E']
        self.classrooms = ['Room_101', 'Room_102', 'Room_103', 'Room_104', 'Room_105']
        
        # Teacher-Subject mapping (which teacher can teach which subject)
        self.teacher_subjects = {
            'Teacher_A': ['Math', 'Physics'],
            'Teacher_B': ['Chemistry', 'Physics'],
            'Teacher_C': ['English', 'History'],
            'Teacher_D': ['Math', 'History'],
            'Teacher_E': ['Chemistry', 'English']
        }
        
        # Subject requirements (how many periods per week)
        self.subject_periods = {
            'Math': 3,
            'Physics': 2,
            'Chemistry': 2,
            'English': 2,
            'History': 1
        }
        
        # Current assignment: (day, time_slot) -> (subject, teacher, classroom)
        self.assignment = {}
        
    def is_valid_assignment(self, day: str, time_slot: str, subject: str, teacher: str, classroom: str) -> bool:
        """Check if an assignment violates any constraints"""
        
        # Check if teacher can teach this subject
        if subject not in self.teacher_subjects[teacher]:
            return False
            
        # Check if teacher is already assigned at this time
        for (d, t), (s, teach, room) in self.assignment.items():
            if d == day and t == time_slot and teach == teacher:
                return False
                
        # Check if classroom is already occupied at this time
        for (d, t), (s, teach, room) in self.assignment.items():
            if d == day and t == time_slot and room == classroom:
                return False
                
        return True
    
    def get_subject_count(self, subject: str) -> int:
        """Count how many times a subject is already scheduled"""
        count = 0
        for (s, teach, room) in self.assignment.values():
            if s == subject:
                count += 1
        return count
    
    def is_complete(self) -> bool:
        """Check if all subjects have been scheduled according to requirements"""
        for subject, required_periods in self.subject_periods.items():
            if self.get_subject_count(subject) < required_periods:
                return False
        return True
    
    def get_unassigned_variables(self) -> List[Tuple[str, str]]:
        """Get list of unassigned time slots"""
        all_slots = [(day, time) for day in self.days for time in self.time_slots]
        assigned_slots = list(self.assignment.keys())
        return [slot for slot in all_slots if slot not in assigned_slots]
    
    def get_domain_values(self, day: str, time_slot: str) -> List[Tuple[str, str, str]]:
        """Get possible values for a time slot (subject, teacher, classroom combinations)"""
        values = []
        
        # Only consider subjects that still need more periods
        needed_subjects = [
            subject for subject, required in self.subject_periods.items()
            if self.get_subject_count(subject) < required
        ]
        
        for subject in needed_subjects:
            for teacher in self.teachers:
                if subject in self.teacher_subjects[teacher]:
                    for classroom in self.classrooms:
                        if self.is_valid_assignment(day, time_slot, subject, teacher, classroom):
                            values.append((subject, teacher, classroom))
        
        return values
    
    def backtrack(self) -> bool:
        """Backtracking algorithm to solve the CSP"""
        if self.is_complete():
            return True
            
        # Choose an unassigned variable (time slot)
        unassigned = self.get_unassigned_variables()
        if not unassigned:
            return self.is_complete()
            
        day, time_slot = unassigned[0]  # Simple variable ordering
        
        # Try all possible values for this variable
        domain_values = self.get_domain_values(day, time_slot)
        random.shuffle(domain_values)  # Add some randomness
        
        for subject, teacher, classroom in domain_values:
            # Make assignment
            self.assignment[(day, time_slot)] = (subject, teacher, classroom)
            
            # Recursively try to complete the assignment
            if self.backtrack():
                return True
                
            # Backtrack: remove the assignment
            del self.assignment[(day, time_slot)]
        
        return False
    
    def solve(self) -> bool:
        """Solve the timetable CSP"""
        self.assignment = {}  # Reset assignment
        return self.backtrack()
    
    def print_timetable(self):
        """Print the timetable in a readable format"""
        if not self.assignment:
            print("No solution found!")
            return
            
        print("\n" + "="*80)
        print("WEEKLY TIMETABLE")
        print("="*80)
        
        # Print header
        print(f"{'Time':<12}", end="")
        for day in self.days:
            print(f"{day:<15}", end="")
        print()
        print("-" * 80)
        
        # Print timetable
        for time_slot in self.time_slots:
            print(f"{time_slot:<12}", end="")
            for day in self.days:
                if (day, time_slot) in self.assignment:
                    subject, teacher, classroom = self.assignment[(day, time_slot)]
                    print(f"{subject:<15}", end="")
                else:
                    print(f"{'FREE':<15}", end="")
            print()
        
        print("\n" + "="*80)
        print("DETAILED SCHEDULE")
        print("="*80)
        
        for (day, time_slot), (subject, teacher, classroom) in sorted(self.assignment.items()):
            print(f"{day} {time_slot}: {subject} - {teacher} - {classroom}")
        
        # Print subject count verification
        print("\n" + "="*40)
        print("SUBJECT PERIOD COUNT")
        print("="*40)
        for subject, required in self.subject_periods.items():
            actual = self.get_subject_count(subject)
            status = "✓" if actual == required else "✗"
            print(f"{subject}: {actual}/{required} {status}")

def main():
    """Main function to demonstrate the timetable CSP"""
    print("Timetable Constraint Satisfaction Problem")
    print("Generating timetable with constraints...")
    
    csp = TimetableCSP()
    
    if csp.solve():
        print("Solution found!")
        csp.print_timetable()
    else:
        print("No solution exists with the given constraints!")
        
    # Try multiple solutions
    print("\n" + "="*50)
    print("Trying to find alternative solutions...")
    print("="*50)
    
    solutions_found = 0
    for attempt in range(5):
        csp_new = TimetableCSP()
        if csp_new.solve():
            solutions_found += 1
            print(f"\nSolution {solutions_found}:")
            # Just print a summary instead of full timetable
            subjects_scheduled = {}
            for (day, time), (subject, teacher, room) in csp_new.assignment.items():
                if subject not in subjects_scheduled:
                    subjects_scheduled[subject] = 0
                subjects_scheduled[subject] += 1
            
            print("Subject distribution:", subjects_scheduled)
    
    print(f"\nTotal solutions found in 5 attempts: {solutions_found}")

if __name__ == "__main__":
    main()