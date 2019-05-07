import React from 'react';
import CoveragePlot from "./Coverage";
import ReadsOverTime from "./ReadsOverTime";
import ReadsPerSample from "./ReadsPerSample";
import ReferenceHeatmap from "./ReferenceHeatmap";

const OverallSummary = ({data, reference, referencePanel, viewOptions}) => {

  return (
    <div id="overallSummaryContainer">
      <div className="panelFlexRow">

        {
          reference ? (
            <CoveragePlot
              className="graphContainer"
              width="35%"
              showReferenceMatches={false}
              data={data}
              reference={reference}
              viewOptions={viewOptions}
            />
          ) : null
        }

        {
          data.all.temporal.length > 1 ? (
            <ReadsOverTime
              className="graphContainer"
              width="22%"
              title={"Mapped reads over time"}
              temporalData={data.all.temporal}
              viewOptions={viewOptions}
            />
          ) : null
        }

        <ReadsPerSample
          className="graphContainer"
          width="18%"
          title="Mapped Reads / Sample"
          data={data}
          viewOptions={viewOptions}
        />

        {
          referencePanel ? (
            <ReferenceHeatmap
              className="graphContainer"
              width="25%"
              title="Reference Matches"
              data={data}
              referencePanel={referencePanel}
            />
          ) : null
        }
      </div>
    </div>
  )
}

export default OverallSummary;
