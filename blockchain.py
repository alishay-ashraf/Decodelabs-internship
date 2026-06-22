from typing import List, Dict, Optional

class Voter:
    def __init__(self):
        self.authorized: bool = False  # Set to True when granted voting rights by chairperson
        self.voted: bool = False       # Tracks double-voting prevention
        self.vote: Optional[int] = None # Stores index of the voted proposal

class Proposal:
    def __init__(self, name: str):
        self.name: str = name
        self.vote_count: int = 0

class DecentralizedVotingSystem:
    def __init__(self, chairperson_address: str, proposal_names: List[str]):
        """
        Initializes a new voting session.
        The creator of the contract becomes the chairperson.
        """
        self.chairperson: str = chairperson_address
        
        # Mapping ledger: keys are simulated cryptographic wallet addresses
        self.voters: Dict[str, Voter] = {}
        
        # State array storing all active proposals
        self.proposals: List[Proposal] = [Proposal(name) for name in proposal_names]
        
        # Automatically initialize a Voter state structure for the chairperson
        self.voters[self.chairperson] = Voter()
        self.voters[self.chairperson].authorized = True

    def give_right_to_vote(self, sender_address: str, voter_address: str):
        """
        Authorizes specific voters to cast ballot tallies.
        Enforces Access Control: Only the digital bouncer (chairperson) can authorize.
        """
        # require(msg.sender == chairperson)
        if sender_address != self.chairperson:
            raise PermissionError("Only the chairperson can authorize voters.")
        
        # Ensure the voter record exists in the mapping ledger
        if voter_address not in self.voters:
            self.voters[voter_address] = Voter()
            
        # require(!voters[voter].voted)
        if self.voters[voter_address].voted:
            raise ValueError("The voter has already voted.")
            
        # require(voters[voter].authorized == False)
        if self.voters[voter_address].authorized:
            raise ValueError("Voter is already authorized.")
            
        # Change state to authorized
        self.voters[voter_address].authorized = True
        print(f"Success: Address {voter_address} has been granted authorization.")

    def cast_vote(self, sender_address: str, proposal_index: int):
        """
        Enforces mechanical state rules and updates proposal counts securely.
        """
        # Ensure voter state exists
        if sender_address not in self.voters:
            self.voters[sender_address] = Voter()
            
        voter_state = self.voters[sender_address]
        
        # require(voters[msg.sender].authorized)
        if not voter_state.authorized:
            raise PermissionError("Unauthorized: You do not have the right to vote.")
            
        # require(!voters[msg.sender].voted)
        if voter_state.voted:
            raise ValueError("Double-voting prevention active: Already voted.")
            
        # require(proposal_index < proposals.length)
        if proposal_index < 0 or proposal_index >= len(self.proposals):
            raise IndexError("Invalid choice: Proposal index out of bounds.")
            
        # State transformation
        voter_state.voted = True
        voter_state.vote = proposal_index
        self.proposals[proposal_index].vote_count += 1
        
        print(f"Success: Vote successfully cast by {sender_address} for proposal '{self.proposals[proposal_index].name}'.")

    def calculate_winning_proposal(self) -> str:
        """
        Uses explicit conditional routing (if/else logic) to calculate 
        the winning proposal index and identify the leading proposal state.
        """
        if not self.proposals:
            return "No proposals found in system state."
            
        winning_vote_count = 0
        winning_index = 0
        
        # Dynamic loop tally calculation using standard control flow
        for index in range(len(self.proposals)):
            if self.proposals[index].vote_count > winning_vote_count:
                winning_vote_count = self.proposals[index].vote_count
                winning_index = index
            else:
                # No state changes if the current proposal count doesn't exceed the leader
                pass
                
        return f"Winning Proposal: {self.proposals[winning_index].name} with {winning_vote_count} votes."


# --- SYSTEM ARCHITECTURE SIMULATION TEST ---
if __name__ == "__main__":
    # Setup addresses
    chairperson = "0xAbC123"
    voter_1 = "0x789dEf"
    voter_2 = "0x456gHi"
    
    # 1. Initialize System State with proposals
    voting_system = DecentralizedVotingSystem(chairperson, ["Proposal A", "Proposal B", "Proposal C"])
    print("--- Voting System Initiated ---")
    
    # 2. Access Control Test: Authorize regular accounts to vote
    voting_system.give_right_to_vote(sender_address=chairperson, voter_address=voter_1)
    voting_system.give_right_to_vote(sender_address=chairperson, voter_address=voter_2)
    
    # 3. Secure State Management: Cast valid votes
    voting_system.cast_vote(sender_address=chairperson, proposal_index=0)  # Chairperson votes Proposal A
    voting_system.cast_vote(sender_address=voter_1, proposal_index=1)     # Voter 1 votes Proposal B
    voting_system.cast_vote(sender_address=voter_2, proposal_index=1)     # Voter 2 votes Proposal B
    
    # 4. Mechanical Logic Validation: Attempt double voting (Should fail)
    print("\n[Security Testing] Attempting Double-Vote...")
    try:
        voting_system.cast_vote(sender_address=voter_1, proposal_index=2)
    except ValueError as error:
        print(f"Execution Stopped & Reverted: {error}")
        
    # 5. Access Control Validation: Attempt unauthorized initialization (Should fail)
    print("\n[Security Testing] Unauthorized user trying to call give_right_to_vote...")
    try:
        voting_system.give_right_to_vote(sender_address=voter_1, voter_address="0xWrong")
    except PermissionError as error:
        print(f"Execution Stopped & Reverted: {error}")

    # 6. Final Tally Result Routing
    print("\n--- Final Dynamic Tally ---")
    result = voting_system.calculate_winning_proposal()
    print(result)