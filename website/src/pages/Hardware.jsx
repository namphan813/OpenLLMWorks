import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import Layout from "../layout/Layout";

function formatScore(value) {
  if (typeof value !== "number") {
    return "Unknown";
  }

  return value.toFixed(2);
}

function formatMemoryConfigurations(system) {
  const configurations = system?.memoryConfigurationsGb;

  if (
    Array.isArray(configurations) &&
    configurations.length > 0
  ) {
    return configurations
      .map((memory) => `${memory} GB`)
      .join(", ");
  }

  return "Unknown";
}

function Hardware() {
  const [hardwareData, setHardwareData] = useState(null);
  const [error, setError] = useState(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [vendorFilter, setVendorFilter] = useState("all");
  const [sortBy, setSortBy] = useState("name");

  useEffect(() => {
    const hardwareDataUrl =
      `${import.meta.env.BASE_URL}hardware.json`;

    async function loadHardwareData() {
      try {
        const response = await fetch(hardwareDataUrl);

        if (!response.ok) {
          throw new Error(
            `Hardware data request failed: ${response.status}`,
          );
        }

        const data = await response.json();

        if (!Array.isArray(data.hardware)) {
          throw new Error(
            "Published hardware data does not contain a hardware list.",
          );
        }

        setHardwareData(data);
      } catch (loadError) {
        console.error(
          "Unable to load published hardware data.",
          loadError,
        );

        setError(loadError);
      }
    }

    loadHardwareData();
  }, []);

  const availableVendors = useMemo(() => {
    if (!hardwareData) {
      return [];
    }

    return [
      ...new Set(
        hardwareData.hardware
          .map((hardware) => hardware.gpuVendor)
          .filter(
            (vendor) =>
              vendor &&
              vendor !== "Unknown",
          ),
      ),
    ].sort((left, right) =>
      left.localeCompare(right),
    );
  }, [hardwareData]);

  const visibleHardware = useMemo(() => {
    if (!hardwareData) {
      return [];
    }

    const normalizedSearch =
      searchQuery.trim().toLowerCase();

    const filtered = hardwareData.hardware.filter(
      (hardware) => {
        const matchesVendor =
          vendorFilter === "all" ||
          hardware.gpuVendor === vendorFilter;

        if (!matchesVendor) {
          return false;
        }

        if (!normalizedSearch) {
          return true;
        }

        const searchableValues = [
          hardware.gpuVendor,
          hardware.gpuModel,
          hardware.gpuIdentity?.vramGib,
          hardware.gpuIdentity?.formFactor,
          hardware.performance.averagePp512,
          hardware.performance.averageTg128,
          hardware.system.averageMemoryGb,
          ...(hardware.system.memoryConfigurationsGb ?? []),
          ...(hardware.system.operatingSystems ?? []),
        ];

        return searchableValues.some(
          (value) =>
            String(value ?? "")
              .toLowerCase()
              .includes(normalizedSearch),
        );
      },
    );

    return [...filtered].sort((left, right) => {
      if (sortBy === "pp512") {
        return (
          (right.performance.averagePp512 ?? -Infinity) -
          (left.performance.averagePp512 ?? -Infinity)
        );
      }

      if (sortBy === "tg128") {
        return (
          (right.performance.averageTg128 ?? -Infinity) -
          (left.performance.averageTg128 ?? -Infinity)
        );
      }

      return left.gpuModel.localeCompare(
        right.gpuModel,
      );
    });
  }, [
    hardwareData,
    searchQuery,
    vendorFilter,
    sortBy,
  ]);

  return (
    <Layout>
      <section className="hardware-page">
        <h1>Hardware</h1>

        <p>
          Explore local LLM benchmark performance across
          community-tested hardware.
        </p>

        {error && (
          <p>
            Hardware data could not be loaded.
          </p>
        )}

        {!hardwareData && !error && (
          <p>
            Loading hardware data...
          </p>
        )}

        {hardwareData && (
          <>
            <p>
              {hardwareData.summary.gpuVariants} GPU variants ·{" "}
              {hardwareData.summary.benchmarkResults} benchmark results
            </p>

            <div className="hardware-controls">
              <label className="hardware-search">
                <span>Search hardware</span>

                <input
                  type="search"
                  value={searchQuery}
                  onChange={(event) =>
                    setSearchQuery(event.target.value)
                  }
                  placeholder="Search GPU, vendor, score, VRAM, OS..."
                />
              </label>

              <div className="hardware-filter-group">
                <label className="hardware-vendor-filter">
                  <span>Vendor</span>

                  <select
                    value={vendorFilter}
                    onChange={(event) =>
                      setVendorFilter(event.target.value)
                    }
                  >
                    <option value="all">
                      All vendors
                    </option>

                    {availableVendors.map((vendor) => (
                      <option
                        key={vendor}
                        value={vendor}
                      >
                        {vendor}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="hardware-sort">
                  <span>Sort by</span>

                  <select
                    value={sortBy}
                    onChange={(event) =>
                      setSortBy(event.target.value)
                    }
                  >
                    <option value="name">
                      GPU name
                    </option>

                    <option value="pp512">
                      Average pp512
                    </option>

                    <option value="tg128">
                      Average tg128
                    </option>
                  </select>
                </label>
              </div>
            </div>

            <p className="hardware-result-count">
              Showing {visibleHardware.length} of{" "}
              {hardwareData.hardware.length} GPU variants
            </p>

            {visibleHardware.length > 0 ? (
              <div className="hardware-list">
                {visibleHardware.map((hardware) => (
                  <Link
                    className="hardware-card-link"
                    key={hardware.variantId}
                    to={`/hardware/${hardware.variantId}`}
                  >
                    <article className="hardware-card">
                      <p className="hardware-card-vendor">
                        {hardware.gpuVendor ?? "Unknown vendor"}
                      </p>

                      <h2>{hardware.gpuModel}</h2>

                      <p>
                        Benchmarks: {hardware.submissionCount}
                      </p>

                      <p>
                        VRAM:{" "}
                        {hardware.gpuIdentity?.vramGib ?? "Unknown"} GiB
                      </p>

                      <p>
                        Tested Memory:{" "}
                        {formatMemoryConfigurations(
                          hardware.system,
                        )}
                      </p>

                      <p>
                        Average pp512:{" "}
                        {formatScore(
                          hardware.performance.averagePp512,
                        )}{" "}
                        tokens/sec
                      </p>

                      <p>
                        Average tg128:{" "}
                        {formatScore(
                          hardware.performance.averageTg128,
                        )}{" "}
                        tokens/sec
                      </p>

                      <p>
                        Operating Systems:{" "}
                        {hardware.system.operatingSystems.length > 0
                          ? hardware.system.operatingSystems.join(", ")
                          : "Unknown"}
                      </p>
                    </article>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="hardware-empty">
                No hardware matches the current filters.
              </p>
            )}
          </>
        )}
      </section>
    </Layout>
  );
}

export default Hardware;