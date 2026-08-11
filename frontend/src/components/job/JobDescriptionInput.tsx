
// src/components/job/JobDescriptionInput.tsx

import {
  useState,
} from "react";

import {
  Card,
  Button,
} from "@/components/common/ui";


interface JobDescriptionInputProps {

  value: string;

  onChange: (
    value: string
  ) => void;

}


export function JobDescriptionInput({

  value,

  onChange,

}: JobDescriptionInputProps) {

  return (

    <Card
      className="
        p-6
        h-full
        flex
        flex-col
      "
    >

      <div
        className="
          flex
          items-center
          justify-between
          mb-1
        "
      >

        <h3
          className="
            text-sm
            font-semibold
          "
        >

          Job Description

        </h3>


        {value.length > 0 && (

          <Button

            variant="ghost"

            size="sm"

            onClick={() =>
              onChange("")
            }

          >

            Clear

          </Button>

        )}

      </div>


      <p
        className="
          text-xs
          text-muted
          mb-4
        "
      >

        Paste the complete job posting
        you're targeting.

      </p>


      <textarea

        value={
          value
        }

        onChange={(event) =>
          onChange(
            event.target.value
          )
        }

        placeholder="
          Paste the job description here...
        "

        className="
          flex-1
          min-h-[220px]
          w-full
          resize-none
          rounded-lg
          border
          border-line
          bg-canvas/40
          px-3.5
          py-3
          text-sm
          text-ink
          placeholder:text-muted/70
          focus:border-accent
          focus:bg-surface
          transition-colors
        "

      />


      <p
        className="
          text-xs
          text-muted
          mt-2
          text-right
        "
      >

        {value.length.toLocaleString()}
        {" "}
        characters

      </p>

    </Card>

  );

}
