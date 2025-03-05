import React, { act, useEffect, useState } from "react";

import classes from "./ManageTeamRegistrations.module.css";
import Header from "../../components/Header";
import { fetchWithAuth } from "../../utils/FetchClient";
import { toast } from "react-toastify";
import LoadingScreen from "../../components/UI/LoadingScreen";
import TeamRegistrationTable from "../../components/AdminPanel/TeamRegistrationTable";

function ManageTeamRegistrationsPage() {
  const [teamRegPending, setTeamRegPending] = useState([]);
  const [teamRegApproved, setTeamRegApproved] = useState([]);
  const [teamRegRejected, setTeamRegRejected] = useState([]);
  const [isFetchingTeamReg, setIsFetchingTeamReg] = useState(false);
  const [activeTab, setActiveTab] = useState("pending");

  const fetchRegistration = async () => {
    try {
      setIsFetchingTeamReg(true);
      const res = await fetchWithAuth("/api/teams/registrations/");
      const data = await res.json();

      if (!res.ok) return toast.error("Failed to fetch team registration!");
      if (res.ok) {
        console.log(data.results);
        const pending = data.results.filter(
          (item) => item.status === "pending"
        );
        const rejected = data.results.filter(
          (item) => item.status === "rejected"
        );
        const approved = data.results.filter(
          (item) => item.status === "approved"
        );

        setTeamRegPending(pending);
        setTeamRegRejected(rejected);
        setTeamRegApproved(approved);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setIsFetchingTeamReg(false);
    }
  };

  useEffect(() => {
    fetchRegistration();
  }, []);

  return (
    <>
      <div className={classes.container}>
        <Header title={"Manage Team Registrations"} />

        <div className={classes.tabsContainer}>
          <button
            type="button"
            className={
              activeTab === "pending"
                ? `${classes.tabsButton} ${classes.active}`
                : classes.tabsButton
            }
            onClick={() => setActiveTab("pending")}
          >
            Pending
          </button>
          <button
            type="button"
            className={
              activeTab === "approved"
                ? `${classes.tabsButton} ${classes.active}`
                : classes.tabsButton
            }
            onClick={() => setActiveTab("approved")}
          >
            Approved
          </button>
          <button
            type="button"
            className={
              activeTab === "rejected"
                ? `${classes.tabsButton} ${classes.active}`
                : classes.tabsButton
            }
            onClick={() => setActiveTab("rejected")}
          >
            Rejected
          </button>
        </div>

        <div className={classes.card}>
          {activeTab === "pending" && (
            <>
              {teamRegPending.length === 0 && (
                <p>No pending registration at the moment.</p>
              )}
              {teamRegPending.length > 0 && (
                <TeamRegistrationTable
                  teamRegList={teamRegPending}
                  onRefetchData={fetchRegistration}
                  isPending
                />
              )}
            </>
          )}
          {activeTab === "approved" && (
            <>
              {teamRegApproved.length === 0 && (
                <p>No approved registration at the moment.</p>
              )}
              {teamRegApproved.length > 0 && (
                <TeamRegistrationTable teamRegList={teamRegApproved} />
              )}
            </>
          )}
          {activeTab === "rejected" && (
            <>
              {teamRegRejected.length === 0 && (
                <p>No rejected registration at the moment.</p>
              )}
              {teamRegRejected.length > 0 && (
                <TeamRegistrationTable teamRegList={teamRegRejected} />
              )}
            </>
          )}
        </div>
      </div>
    </>
  );
}

export default ManageTeamRegistrationsPage;
