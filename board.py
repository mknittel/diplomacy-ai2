from province import Province, SeaProvince, LandProvince

from player import Player, Unit
from parser import Parser
from resolver import Resolver

from actions import Action, Hold, Move, Convoy, Support, Retreat

import random
from datetime import datetime

class Board:
    def __init__(self, filename):
        self.parser = Parser()
        self.players = {}
        self.land_provinces = {}
        self.sea_provinces = {}
        self.num_centers = 0

        players, land_provinces, sea_provinces, coasts, centers = self.parser.read_board(filename)

        self.add_players(players)
        self.add_land(land_provinces)
        self.add_sea(sea_provinces)
        self.add_coasts(coasts)
        self.add_centers(centers)

    def execute_builds(self, filename):
        builds = self.parser.read_builds(filename)
        self.auto_execute_builds(builds)

    def auto_execute_builds(self, builds):
        build = None

        for player_name in builds.keys():
            player_builds = builds[player_name]

            for build in player_builds:
                build_type = build[0]
                unit_type = build[1]
                loc = build[2]

                player = self.players[player_name]

                if build_type == "build":
                    player.build(unit_type, loc)
                else:
                    player.disband(loc)

                self.players[player_name] = player

    def execute_actions(self, filename):
        self.parser.restart()
        self.parser.read_actions(filename)
        holds, moves, convoys, supports = self.parser.get_actions()
        return self.auto_execute_actions(holds, moves, convoys, supports)

    def auto_execute_actions(self, holds, moves, convoys, supports):
        resolver = Resolver(holds, moves, convoys, supports)
        holds, moves, retreats = resolver.resolve_moves()

        retreat_locs = {}

        for retreat in retreats.values():
            player = self.get_player(retreat.loc)
            
            if player.name in retreat_locs.keys():
                retreat_locs[player.name].append(retreat.loc)
            else:
                retreat_locs[player.name] = [retreat.loc]

            player.retreat(retreat.loc)

        for move in moves.values():
            player = self.get_player(move.start)

            player.move(move.start, move.dest)
            self.players[player.name] = player

        return retreat_locs

    def execute_retreats(self, filename):
        retreats = self.parser.read_retreats(filename)
        self.auto_execute_retreats(retreats)

    # Two retreats to the same place become disbands
    def auto_execute_retreats(self, retreats):
        fails = []

        for player_name in retreats.keys():
            player = self.players[player_name]

            for retreat in retreats[player_name]:
                for other_name in retreats.keys():
                    other = self.players[other_name]

                    for other_retreat in retreats[other_name]:
                        if retreat[1] == other_retreat[1] and other_name != player_name:
                            fails.append(retreat)
                            fails.append(other_retreat)

        for player_name in retreats.keys():
            player = self.players[player_name]

            for retreat in retreats[player_name]:
                if retreat in fails:
                    loc = retreat[0]
                    player.disband_retreat(loc)
                else:
                    start = retreat[0]
                    dest = retreat[1]
                
                    player.place_retreat(start, dest)

        for player in self.players.values():
            player.clean_retreats()

    def update_centers(self):
        for player in self.players.values():
            for unit in player.units.values():
                loc = unit.loc

                if loc in self.land_provinces.keys():
                    land = self.land_provinces[loc]

                    if land.has_center:
                        loser_name = self.get_current_owner(land.name)

                        if loser_name in self.players.keys():
                            loser = self.players[loser_name]
                            loser.lose_center(land.name)

                        player.gain_center(land.name)

    def print_provinces(self):
        for province in self.land_provinces.values():
            province.print_data()

        for province in self.sea_provinces.values():
            province.print_data()

    def print_players(self):
        for player in self.players.values():
            player.print_data()

    def print_centers(self):
        print "Provinces with centers:"

        for province in self.land_provinces.values():
            if province.has_center:
                print province.name

    def add_players(self, players):
        for player_list in players:
            player = Player(player_list[0])

            for i in range(1, len(player_list)):
                player.centers += [player_list[i]]
                player.home_centers += [player_list[i]]
                self.num_centers += 1

            self.players[player_list[0]] = player

    def add_land(self, land_provinces):
        for land_list in land_provinces:
            land = LandProvince(land_list[0])

            for i in range(1, len(land_list)):
                land.add_land_neighbor(land_list[i])

            self.land_provinces[land_list[0]] = land

    def add_sea(self, sea_provinces):
        for sea_list in sea_provinces:
            sea = SeaProvince(sea_list[0])

            for i in range(1, len(sea_list)):
                neighbor = sea_list[i]

                if neighbor in self.land_provinces:
                    land = self.land_provinces[neighbor]
                    land.add_sea_neighbor(sea_list[0])
                    self.land_provinces[neighbor] = land

                    sea.add_land_neighbor(neighbor)
                else:
                    sea.add_sea_neighbor(neighbor)

            self.sea_provinces[sea_list[0]] = sea

    def add_coasts(self, coasts):
        for coast_list in coasts:
            land = self.land_provinces[coast_list[0]]
            
            for i in range(1, len(coast_list)):
                land.add_coast(coast_list[i])

            self.land_provinces[coast_list[0]] = land

    def add_centers(self, centers):
        for center_list in centers:
            land = self.land_provinces[center_list[0]]
            land.has_center = True

            self.land_provinces[center_list[0]] = land
            self.num_centers += 1

    def get_player(self, loc):
        for player_name in self.players.keys():
            player = self.players[player_name]

            for unit_loc in player.units.keys():
                if unit_loc == loc:
                    return player

            for unit_loc in player.retreats.keys():
                if unit_loc == loc:
                    return player

        print "Error: invalid unit fetch"
        return None

    def print_moves(self, holds, moves, convoys, supports):
        for hold in holds.values():
            hold.print_action()

        for move in moves.values():
            move.print_action()

        for convoy in convoys.values():
            convoy.print_action()

        for support in supports.values():
            support.print_action()

    def get_all_rand_builds(self, player_name):
        player = self.players[player_name]

        num_units = player.num_units()
        num_centers = player.num_centers()
        num_builds = num_centers - num_units

        builds = {}
        builds[player_name] = []

        if num_builds > 0:
            build_opts = []

            for center in player.home_centers:
                if not self.occupied(center):
                    build_opts.append(center)

            if num_builds > len(build_opts):
                num_builds = len(build_opts)

            random.seed(datetime.now())
            random.shuffle(build_opts)

            for i in range(num_builds):
                loc_name = build_opts[i]
                loc = self.land_provinces[loc_name]

                if loc.landlocked():
                    builds[player_name].append(["build", "army", loc_name])
                else:
                    random.seed(datetime.now())
                    index = random.randint(0,1)

                    if index == 1:
                        builds[player_name].append(["build", "army", loc_name])
                    else:
                        builds[player_name].append(["build", "fleet", loc_name])
        else:
            disband_opts = []
            num_disbands = -num_builds

            for unit in player.units.values():
                disband_opts.append((unit.loc, unit.unit_type))

            random.seed(datetime.now())
            random.shuffle(disband_opts)

            for i in range(num_disbands):
                disband = disband_opts[i]
                builds[player_name].append(["disband", disband[1], disband[0]]) 

        return builds

    def get_all_rand_actions(self, player_name):
        units = []
        holds = {}
        moves = {}
        convoys = {}
        supports = {}
        player = self.players[player_name]

        # Ensure pass by value
        for unit in player.units.values():
            new_unit = Unit(unit.unit_type, unit.loc)
            units.append(unit)

        random.seed(datetime.now())
        random.shuffle(units)

        for unit in units:
            action = self.get_rand_action(unit.loc, unit.unit_type, player_name, holds, moves, convoys, supports)

            if action.action_type == "Hold":
                holds[action.start] = action
            elif action.action_type == "Move":
                moves[action.start] = action
            elif action.action_type == "Convoy":
                convoys[action.start] = action

                start = action.start
            else:
                supports[action.loc] = action

        return holds, moves, convoys, supports

    def get_all_rand_retreats(self, player_name):
        player = self.players[player_name]
        retreats = player.retreats
        orders = {}
        orders[player_name] = []

        keys = retreats.keys()

        random.seed(datetime.now())
        random.shuffle(keys)

        for key in keys:
            unit = player.retreats[key]

            if unit == None:
                continue

            neighbors = self.get_neighbors(unit.loc, unit.unit_type)
            bad_neighbors = []
            
            for neighbor in neighbors:
                if self.occupied(neighbor):
                    bad_neighbors.append(neighbor) 

            for neighbor in bad_neighbors:
                neighbors.remove(neighbor)

            if len(neighbors) > 0:
                random.seed(datetime.now())
                neighbor_index = random.randint(0, len(neighbors) - 1)

                neighbor = neighbors[neighbor_index]
                orders[player_name].append([unit.loc, neighbor])

        return orders

    def get_rand_action(self, loc, unit_type, player_name, holds, moves, convoys, supports):
        all_actions = self.get_all_unit_actions(loc, unit_type, player_name, holds, moves, convoys, supports)

        random.seed(datetime.now())
        index = random.randint(0, len(all_actions) - 1)

        return all_actions[index]

    def get_all_unit_actions(self, loc, unit_type, player_name, holds, moves, convoys, supports):
        neighbors = self.get_neighbors(loc, unit_type)
        unit_actions = []

        # The hold action
        hold = Hold(loc)
        unit_actions.append(hold)

        # All move actions
        for neighbor in neighbors:
            occupied = self.occupied_by_player(neighbor, player_name)
            will_move = self.will_move(neighbor, moves, convoys)
            
            if not occupied or will_move:
                move = Move(loc, neighbor)
                unit_actions.append(move)

        # All convoy actions
        # Note: can only convoy self, can only do single convoys
        if unit_type == "fleet" and loc in self.sea_provinces.keys():
            neighbors = self.get_neighbors(loc, "army")

            for start in neighbors:
                # Get unit to convoy
                if self.occupied_by_player(start, player_name) and not self.in_action(start, holds, moves, convoys, supports):
                    player = self.players[player_name]
                    unit_type = player.get_unit_type(start)

                    if unit_type == "army":
                        for dest in neighbors:
                            if not self.occupied(dest):
                                convoy = Convoy(start, dest, [loc])
                                unit_actions.append(convoy)

        # All support hold actions
        for hold in holds.values():
            if hold.start in neighbors:
                support = Support(loc, hold)
                unit_actions.append(support)

        # All support move actions
        for move in moves.values():
            if move.dest in neighbors:
                support = Support(loc, move)
                unit_actions.append(support)

        # All support convoy actions
        for convoy in convoys.values():
            if convoy.dest in neighbors:
                support = Support(loc, convoy)
                unit_actions.append(support)

        return unit_actions

    def will_move(self, loc, moves, convoys):
        for start in moves.keys():
            if start == loc:
                return True

        for start in convoys.keys():
            if start == loc:
                return True

        return False

    def in_action(self, loc, holds, moves, convoys, supports):
        for hold in holds.keys():
            if hold == loc:
                return True

        for move in moves.keys():
            if move == loc:
                return True

        for convoy in convoys.keys():
            if convoy == loc:
                return True

            convoy_obj = convoys[convoy]

            for fleet in convoy_obj.convoys:
                if fleet == loc:
                    return True

        for support in supports.keys():
            if support == loc:
                return True

        return False

    def get_neighbors(self, loc, unit_type):
        neighbors = []

        if loc in self.land_provinces.keys():
            land = self.land_provinces[loc]
            
            if unit_type == "fleet":
                neighbors = land.fleet_neighbors
            else:
                neighbors = land.army_neighbors
        else:
            sea = self.sea_provinces[loc]

            if unit_type == "fleet":
                neighbors = sea.fleet_neighbors
            else:
                neighbors = sea.army_neighbors
        
        return neighbors
        
    # Occupied by any unit from player
    def occupied_by_player(self, loc, player_name):
        player = self.players[player_name]

        for unit_loc in player.units.keys():
            if unit_loc == loc:
                return True

        return False

    # Occupied by any unit from any player
    def occupied(self, loc):
        for player in self.players.values():
            for unit_loc in player.units.keys():
                if unit_loc == loc:
                    return True

        return False

    def get_winner(self):
        for player in self.players.values():
            num_centers = player.num_centers()
            prop_centers = (1.0 * num_centers) / self.num_centers

            if prop_centers > .529:
                return player.name

        return None

    def get_builds(self):
        builds = []
        build_messages = []

        for player in self.players.values():
            num_units = player.num_units()
            num_centers = player.num_centers()

            num_builds = num_centers - num_units
            builds.append(num_builds)

            if num_builds > 0:
                build_messages.append(player.name + " can build " + str(num_builds) + " units.")
            elif num_builds < 0:
                num_disbands = -num_builds
                build_messages.append(player.name + " must disband " + str(num_disbands) + " units.")
            else:
                build_messages.append(player.name + " has no builds or disbands.")

        return builds, build_messages

    def get_current_owner(self, loc):
        for player in self.players.values():
            if loc in player.centers:
                return player.name

    def get_players(self):
        return self.players.keys()
