from actions import Action, Hold, Move, Convoy, Support, Retreat

class Resolver:
    def __init__(self, holds, moves, convoys, supports):
        self.holds = holds
        self.moves = moves
        self.convoys = convoys
        self.supports = supports
        self.retreats = {}
        self.hold_success = {}
        self.move_success = {} # Includes moves and convoys
        self.dislodged = []

    def resolve_moves(self):
        self.remove_move_swaps()
        self.cut_convoys()
        self.cut_supports()
        self.calculate_powers()
        self.convoys_to_holds()
        self.supports_to_holds()
        self.convoys_to_moves()

        while len(self.holds) != 0 or len(self.moves) != 0:
            self.execute_round()

        for dis in self.dislodged:
            if dis.start in self.hold_success.keys():
                self.hold_success.pop(dis.start, None)

        return self.hold_success, self.move_success, self.retreats

    def remove_move_swaps(self):
        moves_list = self.moves.values()
        remove_list = []

        for i in range(len(moves_list) - 1):
            for j in range(i + 1, len(moves_list)):
                istart = moves_list[i].start
                idest = moves_list[i].dest
                jstart = moves_list[j].start
                jdest = moves_list[j].dest

                if istart == jdest and idest == jstart and i not in remove_list:
                    holdi = Hold(istart)
                    holdj = Hold(jstart)
                    self.holds[istart] = holdi
                    self.holds[jstart] = holdj
                    remove_list += [istart, jstart]

        for start in remove_list:
            self.moves.pop(start, None)

    def cut_convoys(self):
        remove_list = []

        for key in self.convoys.keys():
            convoy = self.convoys[key]
            
            for fleet_loc in convoy.convoys:
                for move in self.moves.values():
                    if move.dest == fleet_loc and key not in remove_list:
                        remove_list.append(key)

        for key in remove_list:
            convoy = self.convoys.pop(key, None)

            hold = Hold(key)
            self.holds[key] = hold

            for fleet_loc in convoy.convoys:
                hold = Hold(fleet_loc)
                self.holds[fleet_loc] = hold

    def cut_supports(self):
        remove_list = []

        for key in self.supports.keys():
            support = self.supports[key]

            for move in self.moves.values():
                if move.dest == key and key not in remove_list:
                    remove_list.append(key)

            for convoy in self.convoys.values():
                if convoy.dest == key and key not in remove_list:
                    remove_list.append(key)

        for key in remove_list:
            support = self.supports.pop(key, None)

            hold = Hold(key)
            self.holds[key] = hold

    def convoys_to_holds(self):
        for convoy in self.convoys.values():
            for fleet_loc in convoy.convoys:
                hold = Hold(fleet_loc)
                self.holds[fleet_loc] = hold

    def supports_to_holds(self):
        for support in self.supports.values():
            hold = Hold(support.loc)
            self.holds[support.loc] = hold

    def convoys_to_moves(self):
        for convoy in self.convoys.values():
            move = Move(convoy.start, convoy.dest)
            self.moves[convoy.start] = move

    def calculate_powers(self):
        for support in self.supports.values():
            start = support.action.start

            if start in self.holds.keys():
                hold = self.holds[start]
                hold.add_power()
                self.holds[start] = hold
            elif start in self.moves.keys():
                move = self.moves[start]
                move.add_power()
                self.moves[start] = move

    def print_powers(self):
        for hold in self.holds.values():
            print "Hold at", hold.start, "has power", hold.action_power
            print "And hold power", hold.hold_power
        for move in self.moves.values():
            print "Move from", move.start, "to", move.dest, "has power", move.action_power
            print "And hold power", move.hold_power

    def get_conflicts(self, loc):
        conflicts = []

        for hold in self.holds.values():
            if hold.start == loc:
                conflicts.append(hold)

        for move in self.moves.values():
            if move.start == loc or move.dest == loc:
                conflicts.append(move)

        return conflicts

    def get_best_action(self, holder, actions):
        if len(actions) == 0:
            return holder, None, True, False

        holder_win = True
        unique_best_action = True
        best_action = None

        if holder == None:
            holder_win = False

        for action in actions:
            if holder != None and action.action_power > holder.hold_power:
                holder_win = False
            
            if best_action != None and action.action_power == best_action.action_power:
                unique_best_action = False
            elif best_action == None or action.action_power > best_action.action_power:
                unique_best_action = True
                best_action = action

        return holder, best_action, holder_win, unique_best_action

    def resolve_loc(self, loc):
        actions = []
        holder = None
        modified = False

        for hold_key in self.holds.keys():
            hold = self.holds[hold_key]
            
            if hold.start == loc:
                holder = hold

        for move_key in self.moves.keys():
            move = self.moves[move_key]

            if move.dest == loc:
                actions.append(move)
            elif move.start == loc:
                holder = move

        holder, best_action, holder_win, unique_best_action = self.get_best_action(holder, actions)

        if unique_best_action:
            for action in actions:
                if action.start != best_action.start:
                    modified = True

                    self.moves.pop(action.start)
                    hold = Hold(action.start)
                    self.holds[action.start] = hold
        else:
            for action in actions:
                modified = True

                self.moves.pop(action.start)
                hold = Hold(action.start)
                self.holds[action.start] = hold

        if holder_win:
            if holder.is_hold:
                modified = True

                self.hold_success[loc] = holder
                self.holds.pop(loc, None)
        else:
            if holder != None and holder.is_hold:
                modified = True
                
                self.holds.pop(loc, None)
                retreat = Retreat(loc)
                self.retreats[loc] = retreat

            if holder != None:
                modified = True
                hold = Hold(loc)
                self.dislodged.append(hold)

        if unique_best_action and not holder_win:
            modified = True

            self.moves.pop(best_action.start)
            self.move_success[loc] = best_action
        elif holder_win and holder.is_hold and best_action != None:
            modified = True

            self.moves.pop(best_action.start, None)
            hold = Hold(best_action.start)
            self.holds[best_action.start] = hold

        return modified

    def resolve_cycle(self):
        # Everything can go to its destination
        for move_key in self.moves.keys():
            move = self.moves.pop(move_key, None)
            self.move_success[move.start] = move

        for hold_key in self.holds.keys():
            hold = self.holds.pop(hold_key, None)
            self.hold_success[hold.start] = hold 
                
    # Assume there are actions left
    def execute_round(self):
        flag = False

        for move in self.moves.values():
            flag = self.resolve_loc(move.dest)

            if flag:
                break

        for hold in self.holds.values():
            flag = self.resolve_loc(hold.start)

            if flag:
                break

        if not flag:
            self.resolve_cycle()
