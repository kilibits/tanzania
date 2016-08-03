package main

type Profile struct {
	Name                string
	Party               string
	Constituency        string
	Phone               string
	Email               string
	ImageURL            string
	MemberType          string
	Address             string
	BirthDate           time
	ID                  int16
	PoliticalExperience []PolHist
	EducationHistory    []EduHist
	EmploymentHistory   []EmpHist
}

type EduHist struct {
	Institution string
	Level       string
	Award       string
	From        int8
	To          int8
}

type EmpHist struct {
	Institution string
	Position    string
	From        int8
	To          int8
}

type PolHist struct {
	Institution string
	Position    string
	From        int8
	To          int8
}

func getProfile() {

}

func getAllProfiles() {

}

func getEmploymentHistory() {

}

func getEducationHistory() {

}

func getPoliticalExperienceHistory() {

}
