import {Component} from '@angular/core';
import {MatSnackBar} from "@angular/material/snack-bar";
import {CorrectionRequest, InferenceService, PredictionRequest} from "../../services/inference.service";

@Component({
  selector: 'app-inference-form',
  templateUrl: './inference-form.component.html',
  styleUrls: ['./inference-form.component.scss']
})
export class InferenceFormComponent  {

  title: string = '';
  tags: Set<string> = new Set<string>();
  newTag: string = '';

  processedTitle: string = '';
  predictedTags: Set<string> = new Set<string>();

  constructor(private _snackBar: MatSnackBar,
              private _inferenceService: InferenceService) {
  }

  query(): void {
    if (this.title.trim() === '') {
      this._snackBar.open('Title is missing!', 'Close', {duration: 3000})
      return;
    }

    let request: PredictionRequest = {
      title: this.title
    }

    this._inferenceService.predict(request).subscribe({
      next: response => {
        this.processedTitle = response.title;
        response.tags.forEach(tag => {
          this.predictedTags.add(tag);
          this.tags.add(tag);
        });
      },
      error: _ => {
        this._snackBar.open('Error has occurred', 'Close', {duration: 3000})
      }
    });

  }

  submitFeedback() {
    let request: CorrectionRequest = {
      title: this.processedTitle,
      predicted: Array.from(this.predictedTags.values()),
      actual: Array.from(this.tags.values())
    }
    this._inferenceService.correctPrediction(request).subscribe({
      next: _ => {
        this._snackBar.open('Thank you!', 'Close', {duration: 3000});
        this.reset()
      },
      error: _ => {
        this._snackBar.open('Error has occurred', 'Close', {duration: 3000})
      }
    });
  }

  reset() {
    this.title = '';
    this.newTag = '';
    this.processedTitle = '';
    this.tags.clear();
    this.predictedTags.clear();
  }

}
