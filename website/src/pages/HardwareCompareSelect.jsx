import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  useNavigate,
} from "react-router-dom";

import Layout from "../layout/Layout";


function HardwareCompareSelect() {
  const navigate = useNavigate();

  const [
    hardwareData,
    setHardwareData,
  ] = useState(null);

  const [
    error,
    setError,
  ] = useState(null);

  const [
    leftVariantId,
    setLeftVariantId,
  ] = useState("");

  const [
    rightVariantId,
    setRightVariantId,
  ] = useState("");


  useEffect(() => {
    const hardwareDataUrl =
      `${import.meta.env.BASE_URL}hardware.json`;

    async function loadHardwareData() {
      try {
        const response = await fetch(
          hardwareDataUrl
        );

        if (!response.ok) {
          throw new Error(
            `Hardware data request failed: ${response.status}`,
          );
        }

        const data =
          await response.json();

        if (
          !Array.isArray(
            data.hardware
          )
        ) {
          throw new Error(
            "Published hardware data does not contain a hardware list.",
          );
        }

        setHardwareData(data);
      } catch (loadError) {
        console.error(
          "Unable to load hardware comparison selector data.",
          loadError,
        );

        setError(loadError);
      }
    }

    loadHardwareData();
  }, []);


  const sortedHardware =
    useMemo(() => {
      if (!hardwareData) {
        return [];
      }

      return [
        ...hardwareData.hardware,
      ].sort(
        (left, right) =>
          left.gpuModel.localeCompare(
            right.gpuModel
          )
      );
    }, [hardwareData]);


  const leftHardware =
    sortedHardware.find(
      (hardware) =>
        hardware.variantId ===
        leftVariantId
    ) ?? null;


  const rightHardware =
    sortedHardware.find(
      (hardware) =>
        hardware.variantId ===
        rightVariantId
    ) ?? null;


  const canCompare =
    leftVariantId &&
    rightVariantId &&
    leftVariantId !== rightVariantId;


  function handleCompare() {
    if (!canCompare) {
      return;
    }

    navigate(
      `/compare/${leftVariantId}/${rightVariantId}`
    );
  }


  return (
    <Layout>
      <section className="hardware-compare-select-page">
        <p className="hardware-profile-eyebrow">
          Hardware Comparison
        </p>

        <h1>
          Compare GPUs
        </h1>

        <p className="hardware-compare-select-intro">
          Choose two community-tested GPUs
          to compare local LLM benchmark
          performance side by side.
        </p>

        {error && (
          <p>
            Hardware comparison data could
            not be loaded.
          </p>
        )}

        {!hardwareData &&
          !error && (
            <p>
              Loading hardware data...
            </p>
          )}

        {hardwareData && (
          <>
            <div className="hardware-compare-select-grid">
              <label className="hardware-compare-select-card">
                <span>
                  GPU 1
                </span>

                <select
                  value={leftVariantId}
                  onChange={(event) =>
                    setLeftVariantId(
                      event.target.value
                    )
                  }
                >
                  <option value="">
                    Select a GPU
                  </option>

                  {sortedHardware.map(
                    (hardware) => (
                      <option
                        key={
                          hardware.variantId
                        }
                        value={
                          hardware.variantId
                        }
                      >
                        {
                          hardware.gpuModel
                        }
                      </option>
                    )
                  )}
                </select>

                {leftHardware && (
                  <div className="hardware-compare-select-summary">
                    <strong>
                      {
                        leftHardware.gpuModel
                      }
                    </strong>

                    <span>
                      {
                        leftHardware.gpuIdentity
                          ?.vramGib ??
                        "Unknown"
                      }{" "}
                      GiB VRAM
                    </span>

                    <span>
                      {
                        leftHardware.submissionCount
                      }{" "}
                      benchmark result
                      {leftHardware.submissionCount ===
                      1
                        ? ""
                        : "s"}
                    </span>
                  </div>
                )}
              </label>

              <div className="hardware-compare-select-vs">
                VS
              </div>

              <label className="hardware-compare-select-card">
                <span>
                  GPU 2
                </span>

                <select
                  value={
                    rightVariantId
                  }
                  onChange={(event) =>
                    setRightVariantId(
                      event.target.value
                    )
                  }
                >
                  <option value="">
                    Select a GPU
                  </option>

                  {sortedHardware.map(
                    (hardware) => (
                      <option
                        key={
                          hardware.variantId
                        }
                        value={
                          hardware.variantId
                        }
                      >
                        {
                          hardware.gpuModel
                        }
                      </option>
                    )
                  )}
                </select>

                {rightHardware && (
                  <div className="hardware-compare-select-summary">
                    <strong>
                      {
                        rightHardware.gpuModel
                      }
                    </strong>

                    <span>
                      {
                        rightHardware.gpuIdentity
                          ?.vramGib ??
                        "Unknown"
                      }{" "}
                      GiB VRAM
                    </span>

                    <span>
                      {
                        rightHardware.submissionCount
                      }{" "}
                      benchmark result
                      {rightHardware.submissionCount ===
                      1
                        ? ""
                        : "s"}
                    </span>
                  </div>
                )}
              </label>
            </div>

            {leftVariantId &&
              rightVariantId &&
              leftVariantId ===
                rightVariantId && (
                <p className="hardware-compare-select-warning">
                  Choose two different GPU
                  variants to compare.
                </p>
              )}

            <button
              type="button"
              className="hardware-compare-select-button"
              disabled={!canCompare}
              onClick={handleCompare}
            >
              Compare GPUs
            </button>

            <p className="hardware-compare-select-count">
              {
                hardwareData.summary
                  .gpuVariants
              }{" "}
              GPU variants currently
              available for comparison.
            </p>
          </>
        )}
      </section>
    </Layout>
  );
}


export default HardwareCompareSelect;