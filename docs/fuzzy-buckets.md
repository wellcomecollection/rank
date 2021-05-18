Adjusting boost fuzzy match
- Doesn't help with date sorting
- helps with Carrots / Parrots
    - turning down the boost from 80 -> something
    
We need to cater for when we recall too much, and someone sorts by date, as this will bring fuzzy matches 

Can't have fuzziness on cross_fields, if we want fuzziness on contriobutor AND title matches we can't

Can't have two multimatch bools on title on contributor, but the operator would need to be OR because ...

Other examples
* Carrots / Parrots


Not fixing typos

Crêpe => Crêpe & Crepe
Crepe =>  Crepe & Crêpe

Another thing to do will be to publish a release note

What are we expecting
* Searches with less results
* More searches with 0 results
* Less complaints about fuzzy recall
* Some transliterated search might not work as well