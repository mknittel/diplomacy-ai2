from province import Province
from province import SeaProvince
from province import LandProvince

from player import Player
from parser import Parser

from actions import Action
from actions import Hold
from actions import Move
from actions import Convoy
from actions import Support

class Board:
    def __init__(self, filename):
        self.players = {}
        self.land_provinces = {}
        self.sea_provinces = {}

        parser = Parser()
        players, land_provinces, sea_provinces, coasts, centers = parser.read_board(filename)

        self.add_players(players)
        self.add_land(land_provinces)
        self.add_sea(sea_provinces)
        self.add_coasts(coasts)
        self.add_centers(centers)

    def execute_actions(self, filename):
        parser = Parser()
        parser.read_actions(filename)
        
        holds, moves, convoys, supports = parser.get_actions()

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

                    sea.add_land_neighbor(neighbor)
                else:
                    sea.add_sea_neighbor(neighbor)

            self.sea_provinces[sea_list[0]] = sea

    def add_coasts(self, coasts):
        for coast_list in coasts:
            land = self.land_provinces[coast_list[0]]
            
            for i in range(1, len(coast_list)):
                land.add_coast(coast_list[0])

            self.land_provinces[coast_list[0]] = land

    def add_centers(self, centers):
        for center_list in centers:
            land = self.land_provinces[center_list[0]]
            land.has_center = True
            self.land_provinces[center_list[0]] = land
