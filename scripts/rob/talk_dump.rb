require 'mongo'
require 'bson'
include Mongo
host = 'localhost'
port = 27017
puts "Connecting to #{host}:#{port}"
client  = MongoClient.new(host, port)

db = client["ouroboros"]

projectsdb 	= db["projects"]
discussions = db["discussions"]
users = db["users"]

projects =  ["spacewarp","plankton", "notes_from_nature", "sunspot", "worms", "milky_way", "radio", "condor", "wise", "war_diary", "bat_detective", "sea_floor", "galaxy_zoo", "cyclone_center", "serengeti", "andromeda","planet_four"]
not_working=[""]
done = ["plankton", "notes_from_nature", "sunspot", "worms", "milky_way", "radio", "condor", "wise", "war_diary", "bat_detective", "sea_floor", "galaxy_zoo", "cyclone_center", "serengeti", "andromeda","planet_four"]

projects.each do |project|
	project_id  = projectsdb.find_one(:name => project)["_id"]
		
	done =0
	File.open("#{project}_discussions.csv", "w") do |f|
		done +=1
		puts "done #{done} of #{total}" if done%1000==0
		f.puts ["discussion_id","focus_id","focus_base_type","focus_type","discussion_name","comment_id","comment_response_to_id","user_id","user_name","user_zooniverse_id","body","tags","mentions","created_at"].join("\t")
		discussions.find(:project_id => project_id).each do |discussion|
			discussion["comments"].each do |comment|
				unless comment["body"].nil?
					user = users.find(:zooniverse_id => comment["user_zooniverse_id"]).first
					f.puts [discussion["_id"], discussion["focus"]["_id"], discussion["focus"]["base_type"], discussion["type"], discussion["name"],
						comment["_id"], comment["response_to_id"], comment["user_id"], comment["user_name"], comment["user_zooniverse_id"],
						comment["body"].gsub("\t","  ").gsub("\n", " ").gsub("\r"," "),comment["tags"].join(";"), comment["mentions"].join(";") , comment["created_at"]].join("\t")
				end
			end
		end
	end
	cmd = `gzip #{project}_discussions.csv`
  	puts "File #{project}_discussions.csv.gz created"
end
