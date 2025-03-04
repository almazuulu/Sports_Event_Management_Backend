import { useEffect, useState } from "react";

import classes from "./MyTeams.module.css";
import Header from "../components/Header";
import TeamTable from "../components/Teams/TeamTable";
import CreateButton from "../components/Button/CreateButton";
import { fetchWithAuth } from "../utils/FetchClient";
import { toast } from "react-toastify";
import LoadingScreen from "../components/UI/LoadingScreen";
import Modal from "../components/UI/Modal";
import NewTeamForm from "../components/Teams/NewTeamForm";

function MyTeamsPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [teams, setTeams] = useState([]);
  const [isFetchingTeams, setIsFetchingTeams] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleCreateNew = () => {
    setIsModalOpen(true);
  };

  const handleSubmit = async (formData) => {
    // const formDataToSend = new FormData();
    // formDataToSend.append("logo", formData.logo); // Append file
    // formDataToSend.append("name", formData.name);
    // formDataToSend.append("description", formData.description);
    // formDataToSend.append("contact_email", formData.contact_email);
    // formDataToSend.append("contact_phone", formData.contact_phone);

    // console.log("formDataToSend: ", formDataToSend);

    try {
      setIsSubmitting(true);
      const response = await fetchWithAuth("/api/teams/teams/", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        toast.error(
          <div>
            <strong>Failed to submit form:</strong>
            <ul>
              {Object.entries(data).map(([field, messages]) => (
                <li key={field}>
                  <strong>{field}:</strong> {messages.join(", ")}
                </li>
              ))}
            </ul>
          </div>
        );
      }

      if (response.ok) {
        toast.success("New team created successfully!");
        fetchMyTeams();
        setIsModalOpen(false);

        return { success: true, data };
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const fetchMyTeams = async () => {
    try {
      setIsFetchingTeams(true);
      const response = await fetchWithAuth("/api/teams/my-teams/");
      const data = await response.json();
      if (!response.ok) return toast.error("Failed to fetch teams");
      if (response.ok) {
        console.log(data.results)
        setTeams(data.results);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetchingTeams(false);
    }
  };

  useEffect(() => {
    fetchMyTeams();
  }, []);

  return (
    <>
      <div className={classes.container}>
        <Header title={"My Teams"} />
        {isFetchingTeams ? (
          <LoadingScreen />
        ) : (
          <div className={classes.card}>
            <section className={classes.sectionButton}>
              <CreateButton onClick={handleCreateNew}>
                Create New Team
              </CreateButton>
            </section>
            {teams.length === 0 && (
              <p>No teams available. Please create a new team.</p>
            )}

            {teams.length > 0 && <TeamTable teams={teams} />}
          </div>
        )}
      </div>

      <Modal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        className={classes.modalContainer}
      >
        <NewTeamForm
          onSubmit={handleSubmit}
          loading={isSubmitting}
          onClose={() => setIsModalOpen(false)}
        />
      </Modal>
    </>
  );
}

export default MyTeamsPage;
