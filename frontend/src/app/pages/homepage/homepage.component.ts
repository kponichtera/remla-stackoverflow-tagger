import {Component, OnInit} from '@angular/core';
import {InferenceService} from "../../services/inference.service";
import {MatSnackBar} from "@angular/material/snack-bar";

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent implements OnInit {

  serviceAvailable = false;
  unrecoverableError = false;

  unlockDelay = 1000;
  unlockDelayMax = 5000;

  constructor(private _snackBar: MatSnackBar,
              private _inferenceService: InferenceService) {
  }

  ngOnInit(): void {
    this.unlockForm();
  }

  unlockForm() {
    this._inferenceService.checkModelPresence().subscribe({
      next: modelPresent => {
        if (modelPresent) {
          // Service is available
          this.serviceAvailable = modelPresent;
        } else {
          // Service unavailable - try again in a moment
          this.backoffUnlock();
        }
      },
      error: err => {
        if (err.status == 503 || err.status == 504) {
          // Service unavailable - try again in a moment
          this.backoffUnlock();
        } else {
          // Something else went wrong
          this.unrecoverableError = true;
          this._snackBar.open('Server error, try again later.')
        }
      }
    });
  }

  private backoffUnlock() {
    if (this.unlockDelay < this.unlockDelayMax) {
      this.unlockDelay *= 2;
    }
    setTimeout(() => this.unlockForm(), this.unlockDelay)
  }

}
