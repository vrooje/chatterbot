require 'mongo'
require 'bson'
require 'mysql2'
require 'csv'
include Mongo

@mysql_client = Mysql2::Client.new(:host => 'localhost', :username => 'root', :password => '', :database => 'big_zooniverse')

def write_row(row)
	sql = "INSERT INTO timeline (created_at, user_id, user_name, project_name, type, subject_id, content) VALUES ('#{row[0]}', '#{row[1]}', '#{row[2].nil? ? "" : Mysql2::Client.escape(row[2])}', '#{row[3]}', '#{row[4]}', '#{row[5]}', '#{row[6]}')"
	res = @mysql_client.query(sql)
end

host = 'localhost'
port = 27017
puts "Connecting to #{host}:#{port}"
client  = MongoClient.new(host, port)

db = client["ouroboros"]
projectsdb 	= db["projects"]
favorites = db["favorites"]

projects = ["spacewarp","plankton", "notes_from_nature", "sunspot", "worms", "milky_way", "radio", "condor", "wise", "war_diary", "bat_detective", "sea_floor", "cyclone_center", "andromeda","planet_four"]

projects.each do |project|
	project_id  = projectsdb.find_one(:name => project)["_id"]

	puts "#{project} favorites"
	favorites.find(:project_id => project_id).each do |f|
		ids  = f["subjects"].nil? ? [""] : f["subjects"].map{|s| s["zooniverse_id"] }
		data = [f["created_at"], f["user_id"], f["user_name"], project, "favorite", ids, ""]
		write_row(data)
		# puts data
	end

end
